document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', (e) => {
        const elTarget = e.target;

        console.log(e.target);
        if (elTarget.classList.contains('comment-expand-toogle')) {
            toogleExpandComment(elTarget);
        }
    });

    const elCommentSubmit = document.querySelectorAll('.comment-submit');

    if (elCommentSubmit.length > 0) {
        elCommentSubmit.forEach(e => {
            e.addEventListener('click', e => {
                submitComment(e.target);
            })
        })
    }

    const formJoinClas = document.querySelector('#form-join-clas');
    
    if (formJoinClas) {
        formJoinClas.addEventListener('submit', e => {
            e.preventDefault();
            joinClas();
        })
    }

    const modalJoinClas = document.querySelector('#modal-join-clas');
    if (modalJoinClas) {
        modalJoinClas.addEventListener('hidden.bs.modal', () => {
            const inputClassCode = document.querySelector('#input_code');
            const invalidFeedback = document.querySelector('#invalid-input_code');
    
            inputClassCode.value = '';
            inputClassCode.classList.remove('is-invalid');
            invalidFeedback.innerText = 'Not find code class';
        })
    }

    const inputDueDate = document.querySelector('#due_date');
    const inputDueTime = document.querySelector('#due_time');

    if (inputDueDate && inputDueTime) {
        const inputDueDatetime = document.querySelector('#due_datetime');
        inputDueDate.addEventListener('change', (e) => {
            if (!inputDueDate.value) {
                inputDueDatetime.value = 'No due time';
            } else {
                inputDueDatetime.value = inputDueDate.value + ' ' + inputDueTime.value;
            }
        });

        inputDueTime.addEventListener('change', (e) => {
            if (!inputDueDate.value) {
                inputDueDatetime.value = 'No due time';
            } else {
                inputDueDatetime.value = inputDueDate.value + ' ' + inputDueTime.value;
            }
        });

        const btnClearDueDateTime = document.querySelector('#btn-clear-due-datetime');
        btnClearDueDateTime.addEventListener('click', (e) => {
            inputDueDate.value = '';
            inputDueTime.value = '';
            inputDueDatetime.value = 'No due time';
        });
    }

});

function submitComment(elTarget) {
    const { elCardMaterial, clasId, id, csrftoken } = cardFetchProperties(elTarget);

    const elInput = elCardMaterial.querySelector('.comment-input');

    fetch(`/${clasId}/materials/${id}/comments`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({
            text: elInput.value
        })
    })
    .then(commonFetchResponse)
    .then(response => {
        console.log(response);
        const isExpand = elCardMaterial.querySelector('.comments-parent').dataset.commentExpand;
        
        getComments(elTarget, isExpand);
        elInput.value = '';
    });
}

function makeComment(username, createdAt,text) {
    const elUsername = document.createElement('span');
    const elCreatedAt = document.createElement('span');
    const elText = document.createElement('div');
    const elParent = document.createElement('div');

    elParent.classList.add('comment', 'mb-2');
    elUsername.classList.add('fw-medium');
    elCreatedAt.classList.add('small', 'text-secondary');

    elUsername.innerText = username + ' ';
    elCreatedAt.innerText = createdAt;
    elText.innerText = text;

    elParent.append(elUsername, elCreatedAt, elText);
    return elParent;
}

function toogleExpandComment(elToogleExpand) {
    const elCommentParent = elToogleExpand.parentElement;
    const isExpand = elCommentParent.dataset.commentExpand;

    if (isExpand === 'true') {
        elToogleExpand.innerText = 'Show all';
        elCommentParent.dataset.commentExpand = 'false';
        getComments(elToogleExpand, false);
    } else {
        elToogleExpand.innerText = 'Show less';
        elCommentParent.dataset.commentExpand = 'true';
        getComments(elToogleExpand, true);
    }

    console.log(elCommentParent.dataset.commentExpand);
    console.log(typeof isExpand);
}

function getComments(elTarget, isExpand) {
    const { elCardMaterial, clasId, id, csrftoken } = cardFetchProperties(elTarget);

    fetch(`/${clasId}/materials/${id}/comments?isAll=${isExpand}`, {
        method: 'GET',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
    })
    .then(commonFetchResponse)
    .then(response => {
        console.log(response);
        const comments = response.data;
        const elCommentParent = elCardMaterial.querySelector('.comments-parent');
        const elComments =  elCommentParent.querySelector('.comments');

        const count = response.count;
        const elToogleExpand = elCardMaterial.querySelector('.comment-expand-toogle');
        console.log(count);

        if (count > 0) {
            elCommentParent.classList.add('card-footer', 'pt-3');
        } else {
            elCommentParent.classList.remove('card-footer', 'pt-3');
        }

        if (count > 3) {
            elToogleExpand.removeAttribute('hidden');
        } else {
            elToogleExpand.setAttribute('hidden', '');
        }
        
        elComments.innerHTML = '';

        comments.forEach(comment => {
            elComments.append(makeComment(comment.author, comment.created_at,comment.text));
        });
    })
}

function joinClas() {
    const clasCode = document.querySelector('#input_code').value;
    const inputSubmitJoinClas = document.querySelector('#input-submit-join-clas');
    const csrftoken = Cookies.get('csrftoken');

    inputSubmitJoinClas.setAttribute('disabled', '');

    fetch('/join', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body:  JSON.stringify({
            clas_code: clasCode
        })
    })
    .then(response => {
        if (response.status === 201) {
            return response.json();
        } else if (response.status === 401) {
            window.location.href = '/login';
            throw Error('Unathorized');
        } else if (response.status === 404) {
            response.json().then(response => {
                const inputClassCode = document.querySelector('#input_code')
                const invalidFeedback = document.querySelector('#invalid-input_code')

                inputClassCode.classList.add('is-invalid')
                invalidFeedback.innerText = response.error
            })
            throw Error('Not Found')
        }

        throw Error();
    })
    .then(response => {
        window.location.href = '/' + response.data.id + '/materials';
    })
    .catch(reason => {
        console.log(reason);
    }).finally(() =>{
        inputSubmitJoinClas.removeAttribute('disabled');
    });
        
}

function cardFetchProperties(elTarget) {
    const elCardMaterial = elTarget.closest('.card-material')
    const clasId = document.querySelector('#page-data').dataset.clasId;
    const id = elCardMaterial.id.split('-')[1];
    const csrftoken = Cookies.get('csrftoken');

    return { elCardMaterial, clasId, id, csrftoken };
}

function commonFetchResponse(response) {
    if (response.status === 201) {
        return response.json();
    } else if (response.status === 401) {
        window.location.href = '/login';
        throw Error('Unathorized');
    }

    throw Error();
}