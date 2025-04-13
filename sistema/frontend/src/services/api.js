const API_URL = process.env.REACT_APP_API_URL;

export async function login(username, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      usuario: username,
      senha: password   
    })
  });

  return await response.json();
}
