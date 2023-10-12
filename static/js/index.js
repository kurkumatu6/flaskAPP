document.querySelector("#nicknameCH").addEventListener("change", function(e){
    console.log(e.currentTarget.checked)
    document.querySelector("#nickname").disabled = !e.currentTarget.checked
})