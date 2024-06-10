function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
    return cookieValue;
};
async function register() {
  const user = document.getElementById("name").value;
  const pass = document.getElementById("pass").value;
  const email = document.getElementById("email").value;

  const response = await fetch('/auth/register/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify({ username: user, password: pass, email: email })
  });

  const data = await response.json();
  console.log(data);
}
const csrftoken = Cookies.get('csrftoken');