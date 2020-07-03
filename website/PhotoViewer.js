var albumBucketName = 'stellavagen-website';

// Initialize the Amazon Cognito credentials provider
AWS.config.region = 'eu-west-1'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'eu-west-1:12054b51-3896-4011-b266-7eac2a5a10a5',
});


// Create a new service object
var s3 = new AWS.S3({
    apiVersion: '2006-03-01',
    params: {Bucket: albumBucketName}
});

// A utility function to create HTML.
function getHtml(template) {
    return template.join('\n');
}


// List the photo albums that exist in the bucket.
function listAlbums() {
    s3.listObjects({Delimiter: '/'}, function (err, data) {
        if (err) {
            return alert('There was an error listing your albums: ' + err.message);
        } else {
            var albums = data.CommonPrefixes.map(function (commonPrefix) {
                var prefix = commonPrefix.Prefix;
                var albumName = decodeURIComponent(prefix.replace('/', ''));
                return getHtml([
                    '<li>',
                    '<button style="margin:5px;" onclick="viewAlbum(\'' + albumName + '\')">',
                    albumName,
                    '</button>',
                    '</li>'
                ]);
            });
            var message = albums.length ?
                getHtml([
                    '<p id="demo">JavaScript can change HTML content.</p>',
                    '<button type="button" onclick=\'document.getElementById("demo").innerHTML = "Hello JavaScript!"\'>Click Me!</button>',
                    '<p>Click on an album name to view it.</p>',
                ]) :
                '<p>You do not have any albums. Please Create album.';
            var htmlTemplate = [
                '<h2>Albums</h2>',
                message,
                '<ul>',
                getHtml(albums),
                '</ul>',
            ]
            document.getElementById('viewer').innerHTML = getHtml(htmlTemplate);
        }
    });
}

// Show the photos that exist in an album.
function viewAlbum(albumName) {
    var albumPhotosKey = encodeURIComponent(albumName) + '/';
    s3.listObjects({Prefix: albumPhotosKey}, function (err, data) {
        if (err) {
            return alert('There was an error viewing your album: ' + err.message);
        }
        // 'this' references the AWS.Response instance that represents the response
        var href = this.request.httpRequest.endpoint.href;
        var bucketUrl = href + albumBucketName + '/';

        var photos = data.Contents.map(function (photo) {
            var photoKey = photo.Key;
            var photoUrl = bucketUrl + encodeURIComponent(photoKey);
            return getHtml([
                '<span>',
                '<div>',
                '<br/>',
                '<img style="width:128px;height:128px;" src="' + photoUrl + '"/>',
                '</div>',
                '<div>',
                '<span>',
                photoKey.replace(albumPhotosKey, ''),
                '</span>',
                '</div>',
                '</span>',
            ]);
        });
        var message = photos.length ?
            '<p>The following photos are present.</p>' :
            '<p>There are no photos in this album.</p>';
        var htmlTemplate = [
            '<div>',
            '<button onclick="listAlbums()">',
            'Back To Albums',
            '</button>',
            '</div>',
            '<h2>',
            'Album: ' + albumName,
            '</h2>',
            message,
            '<div>',
            getHtml(photos),
            '</div>',
            '<h2>',
            'End of Album: ' + albumName,
            '</h2>',
            '<div>',
            '<button onclick="listAlbums()">',
            'Back To Albums',
            '</button>',
            '</div>',
            '<div>',
            'TESTING2',
            '</div>',

        ]
        document.getElementById('viewer').innerHTML = getHtml(htmlTemplate);
        document.getElementsByTagName('img')[0].setAttribute('style', 'display:none;');
    });
}


var opts = {
    angle: -0.2, // The span of the gauge arc
    lineWidth: 0.2, // The line thickness
    radiusScale: 1, // Relative radius
    pointer: {
        length: 0.53, // // Relative to gauge radius
        strokeWidth: 0.035, // The thickness
        color: '#000000' // Fill color
    },
    limitMax: false,     // If false, max value increases automatically if value > maxValue
    limitMin: false,     // If true, the min value of the gauge will be fixed
    colorStart: '#6FADCF',   // Colors
    colorStop: '#8FC0DA',    // just experiment with them
    strokeColor: '#E0E0E0',  // to see which ones work best for you
    generateGradient: true,
    highDpiSupport: true,     // High resolution support
    // renderTicks is Optional
    renderTicks: {
        divisions: 5,
        divWidth: 2.2,
        divLength: 0.7,
        divColor: '#333333',
        subDivisions: 6,
        subLength: 0.5,
        subWidth: 0.6,
        subColor: '#302E66'
    }

};


// var target = document.getElementById('foo'); // your canvas element
// var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
// gauge.maxValue = 10400; // set max gauge value
// gauge.setMinValue(0);  // Prefer setter over gauge.minValue = 0
// gauge.animationSpeed = 43; // set animation speed (32 is default value)
// gauge.set(1450); // set actual value