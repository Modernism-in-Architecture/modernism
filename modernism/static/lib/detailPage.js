const feedImages = document.querySelectorAll('.feed-image');

const addEventListenerToFeedImages = () => {
    feedImages.forEach(feedImage => {
        feedImage.addEventListener('click', event => {
            console.log(feedImage);
            event.preventDefault();
            let href = feedImage.getElementsByTagName("a");
            if (href) {
                // window.location.href = href[0].href
            }
        });
    });
};

addEventListenerToFeedImages();