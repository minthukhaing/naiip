const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");
const hamburger = document.querySelector(".hamburger");

function togglePassword(password,title){
  
  const passwordInput = document.getElementById(password);
  const toggleIcon = document.getElementById(title);
  if (passwordInput.type === "password") {
      passwordInput.type = "text";
      toggleIcon.classList.remove("fa-eye");
      toggleIcon.classList.add("fa-eye-slash");
      toggleIcon.title = "Hide password";
    } else {
      passwordInput.type = "password";
      toggleIcon.classList.remove("fa-eye-slash");
      toggleIcon.classList.add("fa-eye");
      toggleIcon.title = "Show password";
    }
}

function toggleSidebar() {
  sidebar.classList.toggle("active");
  overlay.classList.toggle("active");
  hamburger.classList.toggle("active");
}

// tab controll
const tabButtons = document.querySelectorAll(".tab-btn");
const tabContents = document.querySelectorAll(".tab-content");

tabButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const targetTab = button.getAttribute("data-tab");

    tabButtons.forEach((btn) => btn.classList.remove("active"));
    tabContents.forEach((content) => content.classList.remove("active"));

    button.classList.add("active");
    document.getElementById(targetTab).classList.add("active");
  });
});

function copy(id, messageId) {

  const copyText = document.getElementById(id);
  copyText.select();
  document.execCommand("copy");

  const message = document.getElementById(messageId);
  message.style.display = "inline";
  setTimeout(() => {
    message.style.display = "none";
  }, 2000);
}

// copy mm text
document.getElementById("btn-copyMMtext").addEventListener("click", function () {
  const input = document.getElementById("mmconvert");
  input.select();
  input.setSelectionRange(0, 99999); // မိုဘိုင်းအတွက်
  document.execCommand("copy");

  const message = document.getElementById("copy-message");
  message.style.display = "inline";
  setTimeout(() => {
    message.style.display = "none";
  }, 2000);
});

// copy parli text
document.getElementById("btn-copyParlitext").addEventListener("click", function () {
  const input = document.getElementById("parliconvert");
  input.select();
  input.setSelectionRange(0, 99999); // မိုဘိုင်းအတွက်
  document.execCommand("copy");

  const message = document.getElementById("copy-message1");
  message.style.display = "inline";
  setTimeout(() => {
    message.style.display = "none";
  }, 2000);
});
