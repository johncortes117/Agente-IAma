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

        if (!response.ok) {
            throw new Error(data.detail || 'Error en el registro');
        }

        // Guardar datos en localStorage
        localStorage.setItem('userId', data.id);
        localStorage.setItem('userData', JSON.stringify(userData));
        
        // Redirección explícita al test
        window.location.replace('/test');
        return false;
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error en el registro: ' + error.message);
        return false;
    }
}

// Asegurarnos que la función está disponible globalmente
window.handleRegister = handleRegister;
