const nasaImage = document.getElementById('nasaPicture')
fetch(
  'https://api.nasa.gov/planetary/apod?api_key=PI5Fhlc0LjXWmwlekt1BpxTSfixkveFg8NQGI8FA'
)
  .then((data) => data.json())
  .then(({ url, title }) => {
    nasaImage.setAttribute('src', url)
    nasaImage.setAttribute('alt', `The NASA Picture of the Day - "${title}"`)
  })
