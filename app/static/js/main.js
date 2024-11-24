// Función para manejar el registro de usuarios
async function handleRegister(event) {
    event.preventDefault();
    
    const userData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        age: parseInt(document.getElementById('age').value),
        country: document.getElementById('country').value
    };

    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();

        if (response.ok) {
            // Guardar datos del usuario en localStorage
            localStorage.setItem('userData', JSON.stringify(userData));
            localStorage.setItem('userId', data.id);
            
            // Redirigir al chat-interface
            window.location.href = '/chat';
        } else {
            alert(`Error: ${data.detail || 'Error en el registro'}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error en el registro');
    }
}
