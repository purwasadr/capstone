document.addEventListener('DOMContentLoaded', function() {

    document.addEventListener('click', (e) => {
        const elTarget = e.target;

        if (elTarget.classList.contains('comment-submit')) {
            submitComment(elTarget);
        } else if (elTarget.classList.contains('comment-expand-toogle')) {
            toogleExpandComment(elTarget);
        }
    });
});
// document.querySelector('#sss').children
function submitComment(elTarget) {
    const { elCardMaterial, roomId, id, csrftoken } = commonFetchProperties(elTarget);

    const elInput = elTarget.parentElement.querySelector('.comment-input')

    fetch(`/${roomId}/materials/${id}/comments`, {
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
        const comments = response.data;
        const elCommentParent = elCardMaterial.querySelector('.comments-parent');

        console.log(elCommentParent);

        elCommentParent.querySelector('.comments').innerHTML = '';

        console.log(comments);

        console.log('akhirwww');

        comments.forEach(comment => {
            elCommentParent.append(makeComment(comment.author, comment.created_at,comment.text))
        });
    })
}

function makeComment(username, createdAt,text) {
    const elUsername = document.createElement('span');
    const elCreatedAt = document.createElement('span');
    const elText = document.createElement('div');
    const elParent = document.createElement('div');

    elParent.classList.add('comment', 'mb-2');
    elUsername.classList.add('fw-medium');
    elCreatedAt.classList.add('small');

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
        elToogleExpand.innerText = 'Show all'
        elCommentParent.dataset.commentExpand = 'false';
        getComments(elToogleExpand, false);
    } else {
        elToogleExpand.innerText = 'Show less'
        elCommentParent.dataset.commentExpand = 'true';
        getComments(elToogleExpand, true);
    }

    console.log(elCommentParent.dataset.commentExpand);
    console.log(typeof isExpand);
}

function getComments(elToogleExpand, isExpand) {
    const { elCardMaterial, roomId, id, csrftoken } = commonFetchProperties(elToogleExpand);

    fetch(`/${roomId}/materials/${id}/comments?isAll=${isExpand}`, {
        method: 'GET',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
    })
    .then(commonFetchResponse)
    .then(response => {
        console.log(response);
        const comments = response.data;
        const elCommentParent = elCardMaterial.querySelector('.comments-parent');
        const elComments =  elCommentParent.querySelector('.comments')
        
        elComments.innerHTML = '';

        comments.forEach(comment => {
            elComments.append(makeComment(comment.author, comment.created_at,comment.text))
        });
    })
}

function commonFetchProperties(elTarget) {
    const elCardMaterial = elTarget.closest('.card-material')
    const roomId = document.querySelector('#page-data').dataset.roomId;
    const id = elCardMaterial.id.split('-')[1];
    const csrftoken = Cookies.get('csrftoken');

    return { elCardMaterial, roomId, id, csrftoken };
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