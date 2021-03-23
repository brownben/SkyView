const scrollToImage = (image) => {
  if (image.scrollIntoViewIfNeeded) {
    image.scrollIntoViewIfNeeded()
  } else if (image.scrollIntoView) {
    image.scrollIntoView()
  }
}

const getRelativePlanet = (hash, relativeIndex) => {
  const planets = [...document.querySelectorAll('.carousel__item')]
  const indexOfCurrent = planets.findIndex(
    (element) => element.id == hash.slice(1)
  )

  let fallback = planets[0]
  if (relativeIndex > 0) fallback = planets[planets.length - 1]

  return planets?.[indexOfCurrent + relativeIndex] ?? fallback
}

document.querySelector('#controls').addEventListener('click', (event) => {
  const idOfImage = event.target.getAttribute('href')
  const image = document.querySelector(idOfImage)
  history.pushState('', '', `${idOfImage}`)
  if (!image) return

  if (image.scrollIntoViewIfNeeded) {
    event.preventDefault()
    image.scrollIntoViewIfNeeded()
  } else if (image.scrollIntoView) {
    event.preventDefault()
    image.scrollIntoView()
  }
})

document.getElementById('next').addEventListener('click', (event) => {
  const currentId = location.hash
  const newPlanet = getRelativePlanet(currentId, 1)

  scrollToImage(newPlanet)
  history.pushState('', '', `#${newPlanet.id}`)
})

document.getElementById('previous').addEventListener('click', (event) => {
  const currentId = location.hash
  const newPlanet = getRelativePlanet(currentId, -1)

  scrollToImage(newPlanet)
  history.pushState('', '', `#${newPlanet.id}`)
})
