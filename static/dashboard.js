function quizalert(form) {
    swal({
        text: "Remember that quizzes are meant to be enjoyable—keep the atmosphere light and friendly!",
        icon: "/static/images/POPUP.jpg",
        button: "OK",
      })
      .then((isokay) => {
        if (isokay){
            form.submit()
        }
      });
      return false;
}
function funfact1() {
  swal({
      text: "We forget around 50% of what we learn within an hour of learning it—unless we actively practice or recall it.",
      icon: "/static/images/POPUP.jpg",
      button: "OK",
    });
}
function funfact2() {
  swal({
      text: "Learning something new rewires your brain and creates new neural pathways. It's like exercise, but for your mind.",
      icon: "/static/images/POPUP.jpg",
      button: "OK",
    });
}