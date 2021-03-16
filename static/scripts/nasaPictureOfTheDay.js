const createIframe = (url) => {
  const iframe = document.createElement('iframe')
  iframe.setAttribute('src', url + ';modestbranding=1')
  iframe.setAttribute('frameborder', '0')
  iframe.setAttribute('allowfullscreen', true)
  iframe.setAttribute('width', '560')
  iframe.setAttribute('height', '315')
  iframe.setAttribute('id', 'nasaPicture')
  return iframe
}

const createImage = (url, title) => {
  const image = document.createElement('img')
  image.setAttribute('src', url)
  image.setAttribute('alt', `The NASA Picture of the Day - "${title}"`)
  image.setAttribute('id', 'nasaPicture')
  return image
}

const createCorrectContainer = (url, title) => {
  if (url.includes('youtube.com')) return createIframe(url)
  else return createImage(url, title)
}

const getNASAData = async () => {
  const data = await fetch(
    'https://api.nasa.gov/planetary/apod?api_key=PI5Fhlc0LjXWmwlekt1BpxTSfixkveFg8NQGI8FA'
  )
  return data.json()
}

const insertPictureOfTheDay = async () => {
  const nasaPictureContainer = document.getElementById('nasaPictureContainer')
  const { url, title } = await getNASAData()
  const container = createCorrectContainer(url, title)
  nasaPictureContainer.appendChild(container)
}

insertPictureOfTheDay()
