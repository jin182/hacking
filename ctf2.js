$.ajax({
  url: '/api/greet?name=dev&type=admin',
  success: function(response) {
    console.log('Success:', response);
    alert(response);
  },
  error: function() {
    console.log('Error occurred');
  }
});
