$deleteBtn = $(".delete-btn")


$deleteBtn.on('click', function(e){
    let result = confirm("Are you sure you want to delete this? This cannot be undone.")

    if(!result) {
        e.preventDefault();
    }
})