
# youtube-transcriber-api

Youtube's official API currently does not support fetching of a video's transcript. This project is a RESTful API built on top of [jdepoix's API](https://github.com/jdepoix/youtube-transcript-api), and provides simple HTTP endpoints for retrieving pure-text transcripts for YouTube videos. It also provides the ability to translate transcripts into different languages.

# Run with docker

To spin up a container with the image published on Docker Hub, you can use the following Docker command:

```
docker run -p 5000:5000 kelter/youtube-transcriber-api
```

Explanation of the command:

`docker run`: This command is used to run a container from a Docker image.
`-p 5000:5000`: This flag maps port `5000` on your host machine to port `5000` on the container. It allows you to access the service running inside the container at `http://localhost:5000`.
`kelter/youtube-transcriber-api`: This is the name of the Docker image you want to run.

Make sure that you have Docker installed on your machine, and this command should start a container running a Flask application.
If you want to run the container in the background (detached mode), you can add the `-d` flag:

    docker run -d -p 5000:5000 kelter/youtube-transcriber-api

This will run the container in the background, and you'll get your command prompt back.



## API Endpoints

Note: All language codes used should follow the **[ISO 639-1](https://www.w3schools.com/tags/ref_language_codes.asp)** standard (case-sensitive)

### Transcripts

```
GET /v1/transcripts{{id}}
```

Retrieve transcripts for a specified YouTube video.
(try: https://youtube-transcriber-api.vercel.app/v1/transcripts?id=k_GM1JA608Y&lang=en)

**Query Parameters**

| Parameter | Required | Note                                                                                                                                                                 |
| --------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`      | Yes      | The ID of the YouTube video                                                                                                                                          |
| `lang`    | No       | The language code for the desired transcript. If no language is specified, all available transcripts will be returned                                                |
| `type`    | No       | The desired output format. Accepts `json`, `text`, `srt`, and `webvtt`. Default to `text` if not specified                                                           |
| `lb`      | No       | Boolean (0 or 1) indicating whether the transcript should contain line breaks. Only applies for type `text`. Default to 0 if not specified                           |
| `sfx`     | No       | Boolean (0 or 1) indicating whether the transcript should contain sound effects information eg. \[Cheering\], \[Applause\], \[Music\]. Default to 0 if not specified |

**Response**

The request returns a JSON object containing the following fields:

| Field         | Description                                                                                                                                                                                                                                                                                                                                                                   |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `video_id`    | The ID of the YouTube video                                                                                                                                                                                                                                                                                                                                                   |
| `transcripts` | A list of transcripts. Each transcript has the following fields:<br><br>`language`: The language of the transcript<br>`languageCode`: The ISO 639-1 code<br>`isGenerated`: Boolean indicating whether the transcript is machine-generated <br>`isTranslatable`: Boolean indicating whether the transcript can be translated<br>`text`: The transcript in the specified format |

### Translation

```
GET /v1/translations{{id}}{{lang}}
```

Retrieve a translated transcript for a specified YouTube video.
(try: https://youtube-transcriber-api.vercel.app/v1/transcripts?id=k_GM1JA608Y&lang=es)

**Query Parameters**
| Parameter | Required | Note |
|-----------|----------|-------------------------------------------|
| `id` | Yes | The ID of the YouTube video |
| `lang` | Yes | The language code for the target language |

**Response**

The request returns a JSON object containing the following fields:

| Field            | Description                                 |
| ---------------- | ------------------------------------------- |
| `video_id`       | The ID of the YouTube video                 |
| `sourceLanguage` | The language code of the source transcript  |
| `targetLanguage` | The language code of the target translation |
| `transcripts`    | The transcript text                         |

### Metadata

```
GET /v1/metadata{{id}}
```

Retrieve transcript metadata for a specified YouTube video.
(try: https://youtube-transcriber-api.vercel.app/v1/metadata?id=k_GM1JA608Y)

**Query Parameters**

| Parameter | Required | Note                        |
| --------- | -------- | --------------------------- |
| `id`      | Yes      | The ID of the YouTube video |

**Response**

The request returns a JSON object containing the following fields:

| Field         | Description                                                                                                                                                                                                                                                                                                                      |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `video_id`    | The ID of the YouTube video.                                                                                                                                                                                                                                                                                                     |
| `transcripts` | A list of transcript metadata. Each item has the following fields:<br><br>`language`: The language of the transcription<br>`languageCode`: The ISO 639-1 code<br>`isGenerated`: Boolean indicating whether the transcript is machine-generated <br>`isTranslatable`: Boolean indicating whether the transcript can be translated |

## Future Plans
- Add rate limitating
- Migrate from flask (WSGI) to FastAPI (ASGI)

## Donation

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/miguelantunes)

## License

[See license](https://github.com/kelter/youtube-transcriber-api/blob/main/LICENSE)
