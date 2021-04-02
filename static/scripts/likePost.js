const likePost = async ({ likeAPILocation, userId, csrfToken }) => {
  const response = await fetch(likeAPILocation, {
    method: 'POST',
    body: { userId },
    credentials: 'same-origin',
    headers: {
      'X-CSRFToken': csrfToken,
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  })

  const { buttonText, liked, numberOfLikes } = await response.json()
  document.getElementById('like-button-text').innerText = buttonText
  document.getElementById('like-button').classList.toggle('like', liked)
  document.getElementById('number-of-likes').innerText = numberOfLikes
}

// make accessible to template outside of JS module
window.likePost = likePost
