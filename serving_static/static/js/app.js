function AppStart() {

    const editButton = document.getElementById("edit");
    editButton.addEventListener("click", deleteStudent);

    const deleteButton = document.getElementById("delete");
    deleteButton.addEventListener("click", deleteStudent); 



    function deleteStudent() {
      
        return fetch(window.location {
            method: 'DELETE',
        }).then(response => response.json())
    }
}

AppStart()