const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");

const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".invalid_emailFeeback");

const usernameSuccessNotify = document.querySelector(".usernameSuccessNotify")

const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#passwordField");





const handleTooglePassword = (e)=>{

    if(showPasswordToggle.textContent === "SHOW"){
        showPasswordToggle.textContent = "HIDE";

        passwordField.setAttribute("type","text");

    }else{
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type","password");

    }
};


showPasswordToggle.addEventListener("click", handleTooglePassword);



emailField.addEventListener("keyup",(e)=>{
    const emailVal = e.target.value;

    emailField.classList.remove('is-invalid');
    emailField.classList.remove('is-valid');
    emailFeedBackArea.style.display="none";

    if (emailVal.length>0){
        fetch("/authentication/validate-email",{
            body: JSON.stringify({email:emailVal}),
            method:"POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
            if(data.email_error){
                emailField.classList.add('is-invalid');
                emailFeedBackArea.style.display="block";
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`
            }else{
                emailField.classList.add('is-valid');
            }
        });
    }
});

usernameField.addEventListener("keyup",(e)=>{
    
    const usernameVal = e.target.value;
    usernameSuccessNotify.textContent = `Checking: ${usernameVal}`;
    usernameField.classList.remove('is-invalid');
    usernameField.classList.remove('is-valid');
    feedBackArea.style.display="none";

    if (usernameVal.length>0){
        fetch("/authentication/validate-username",{
            body: JSON.stringify({username:usernameVal}),
            method:"POST",
        })
        .then((res)=>res.json())
        .then((data)=>{
            usernameSuccessNotify.style.display = "none";
            if(data.username_error){
                usernameField.classList.add('is-invalid');
                feedBackArea.style.display="block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`
            }else{
                usernameField.classList.add('is-valid');
            }
        });
    }

});
