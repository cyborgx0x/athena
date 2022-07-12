FB.getLoginStatus(function(response) {
    if (response.status === 'connected') {
      console.log(response.authResponse.accessToken);
      axios.post('/login', {
        token: response.authResponse.accessToken
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    }
  });
