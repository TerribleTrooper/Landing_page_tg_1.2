async function send(){

  const data = {
    name: document.getElementById("name").value,
    company: document.getElementById("company").value,
    phone: document.getElementById("phone").value,
    email: document.getElementById("email").value,
    message: document.getElementById("message").value
  };

  console.log("Отправка:", data);

  const res = await fetch("http://localhost:8000/api/lead", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  const result = document.getElementById("result");

  if (res.ok) {
    result.innerText = "Заявка отправлена ✅";
  } else {
    const err = await res.text();
    console.log("Ошибка сервера:", err);
    result.innerText = "Ошибка ❌";
  }
}