window.addEventListener('load', () => {
    const userId = localStorage.getItem('userId');
    const userData = localStorage.getItem('userData');
    
    if (!userId || !userData) {
        window.location.replace('/register');
        return;
    }
    
    // Iniciar el chat solo si el usuario completó el test
    checkTestCompletion(userId);
});

async function checkTestCompletion(userId) {
    try {
        const response = await fetch(`/api/users/${userId}/test-status`);
        const data = await response.json();
        
        if (!data.test_completed) {
            window.location.replace('/test');
        }
    } catch (error) {
        console.error('Error:', error);
        window.location.replace('/test');
    }
} 