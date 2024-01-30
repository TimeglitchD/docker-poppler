# Docker Poppler

A simple http api service for converting pdf to svg, include `inkscape`, `pdftocairo`, `pdfinfo`, `pdftotext`

## Usage

pull the docker image
```
docker pull timeglitchd/svgtopdf
```

start a http server
```
docker run --rm -p 5000:5000 timeglitchd/svgtopdf
```

convert a pdf file to multiple svg via inkscape
```
http -f POST :5000/inkscape file@/path/to/file.pdf
```

convert a pdf file to multiple svg via pdftocairo
```
http -f POST :5000/pdftocairo file@/path/to/file.pdf
```

get a pdf file information
```
http -f POST :5000/pdfinfo file@/path/to/file.pdf
```

convert a pdf file to the text string
```
http -f POST :5000/pdftotext file@/path/to/file.pdf
```