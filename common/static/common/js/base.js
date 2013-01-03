function addCSRFToken(jqXHR) {
    jqXHR.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
}
