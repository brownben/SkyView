document.querySelector('#controls').addEventListener('click', (event) => {
  const idOfImage = event.target.getAttribute('href')
  const image = document.querySelector(idOfImage)

  if (!image) return

  if (image.scrollIntoViewIfNeeded) {
    event.preventDefault()
    image.scrollIntoViewIfNeeded()
  } else if (image.scrollIntoView) {
    event.preventDefault()
    image.scrollIntoView()
  }
})
