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

  const { buttonText } = await response.json()
  document.getElementById('like-button').innerText = buttonText
}

// make accessible to template outside of JS module
window.likePost = likePost
