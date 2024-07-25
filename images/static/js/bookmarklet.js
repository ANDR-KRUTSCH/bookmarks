const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWidth = 250;
const minHeight = 250;

let head = window.document.querySelector('head');
let link = window.document.createElement('link');
link.rel = 'stylesheet';
link.href = styleUrl + '?r=' + Math.floor(Math.random() * 9999999999999999);
head.appendChild(link)

let body = window.document.querySelector('body');
let boxHTML = '<div id="bookmarklet"><a href="#" id="close">x</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
body.innerHTML += boxHTML;

function bookmarkletLaunch() {
    let bookmarklet = window.document.querySelector('#bookmarklet');
    let imagesFound = bookmarklet.querySelector('.images');

    imagesFound.innerHTML = '';
    bookmarklet.style.display = 'block';

    bookmarklet.querySelector('#close').addEventListener('pointerdown', function() {
        bookmarklet.style.display = 'none';
    });

    let images = window.document.querySelectorAll('img[src$="jpg"], img[src$=".jpeg"], img[src$=".png"]');

    images.forEach(image => {
        if (image.naturalHeight >= minHeight && image.naturalWidth >= minWidth) {
            let imageFound = window.document.createElement('img');
            imageFound.src = image.src;
            imagesFound.append(imageFound);
        };
    });

    imagesFound.querySelectorAll('img').forEach(image => {
        image.addEventListener('pointerdown', function(event) {
            let image_selected = event.target;
            bookmarklet.style.display = 'none';
            window.open(siteUrl + 'images/create/?url=' + encodeURIComponent(image_selected.src) + '&title=' + encodeURIComponent(window.document.title) + '_blank');
        });
    });
};

bookmarkletLaunch();