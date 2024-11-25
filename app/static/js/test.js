const questions = [
    {
        id: 1,
        text: "¿Qué asignaturas disfrutas más en la escuela?",
        type: "multiple",
        options: ["Matemáticas", "Ciencias Naturales", "Historia", "Lenguas", "Artes", "Educación Física", "Computación o Tecnología"],
        maxSelections: 3
    },
    {
        id: 2,
        text: "¿En qué asignaturas crees que tienes mejor rendimiento?",
        type: "multiple",
        options: ["Matemáticas", "Ciencias Naturales", "Historia", "Lenguas", "Artes", "Educación Física", "Computación o Tecnología"]
    },
    {
        id: 3,
        text: "¿Prefieres trabajar con números, palabras o conceptos abstractos?",
        type: "multiple",
        options: ["Números", "Palabras", "Conceptos abstractos"]
    },
    {
        id: 4,
        text: "¿Qué actividades disfrutas en tu tiempo libre?",
        type: "multiple",
        options: ["Leer", "Escribir", "Investigar", "Programar", "Crear arte", "Hacer deportes", "Resolver problemas o acertijos"]
    },
    {
        id: 5,
        text: "¿Qué tipo de trabajo te gustaría realizar en el futuro?",
        type: "multiple",
        options: ["Tecnología", "Salud", "Negocios", "Educación", "Creativo", "Investigación científica", "Administración o gestión"]
    },
    {
        id: 6,
        text: "¿Prefieres trabajar en equipo o de forma individual?",
        type: "single",
        options: ["En equipo", "De forma individual"]
    },
    {
        id: 7,
        text: "¿Te consideras una persona más lógica o creativa?",
        type: "single",
        options: ["Lógica", "Creativa"]
    },
    {
        id: 8,
        text: "¿Qué aspectos del trabajo son más importantes para ti?",
        type: "text"
    },
    {
        id: 9,
        text: "¿Qué metas personales o profesionales te gustaría alcanzar en los próximos años?",
        type: "text"
    }
];

let currentQuestion = 0;
const responses = {};
const userId = localStorage.getItem('userId');

function updateProgressBar() {
    const progress = (currentQuestion / questions.length) * 100;
    document.querySelector('.progress').style.width = `${progress}%`;
}

function createQuestionElement(question) {
    const container = document.createElement('div');
    container.className = 'question';

    const title = document.createElement('h2');
    title.textContent = question.text;
    container.appendChild(title);

    if (question.type === "multiple" || question.type === "single") {
        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'options-container';

        question.options.forEach(option => {
            const label = document.createElement('label');
            label.className = 'option-label';

            const input = document.createElement('input');
            input.type = question.type === "multiple" ? 'checkbox' : 'radio';
            input.name = `question-${question.id}`;
            input.value = option;

            if (responses[question.id] && responses[question.id].includes(option)) {
                input.checked = true;
            }

            if (question.type === "multiple" && question.maxSelections) {
                input.addEventListener('change', () => {
                    const checked = optionsContainer.querySelectorAll('input:checked');
                    if (checked.length > question.maxSelections) {
                        input.checked = false;
                    }
                });
            }

            label.appendChild(input);
            label.appendChild(document.createTextNode(option));
            optionsContainer.appendChild(label);
        });

        container.appendChild(optionsContainer);
    } else if (question.type === "text") {
        const textarea = document.createElement('textarea');
        textarea.className = 'text-response';
        textarea.placeholder = "Escribe tu respuesta aquí...";
        textarea.rows = 4;
        
        if (responses[question.id]) {
            textarea.value = responses[question.id][0];
        }
        
        container.appendChild(textarea);
    }

    return container;
}

async function saveResponse() {
    const question = questions[currentQuestion];
    let response;

    if (question.type === "text") {
        const textarea = document.querySelector('.text-response');
        if (!textarea.value.trim()) {
            alert('Por favor, responde la pregunta antes de continuar.');
            return false;
        }
        response = [textarea.value];
    } else {
        const inputs = document.querySelectorAll('input:checked');
        if (inputs.length === 0) {
            alert('Por favor, selecciona al menos una opción.');
            return false;
        }
        response = Array.from(inputs).map(input => input.value);
    }

    try {
        const userId = parseInt(localStorage.getItem('userId'));
        
        const res = await fetch('/api/test/response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                question_id: question.id,
                response: response
            })
        });

        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.detail || 'Error al guardar la respuesta');
        }

        responses[question.id] = response;
        return true;
    } catch (error) {
        console.error('Error:', error);
        alert('Error al guardar la respuesta: ' + error.message);
        return false;
    }
}

async function completeTest() {
    try {
        const res = await fetch(`/api/test/complete/${userId}`, {
            method: 'POST'
        });

        if (!res.ok) {
            throw new Error('Error al completar el test');
        }

        window.location.href = '/chat';
    } catch (error) {
        console.error('Error:', error);
        alert('Error al completar el test');
    }
}

async function handleNavigation(direction) {
    if (direction === 'next' && currentQuestion < questions.length) {
        await saveResponse();
        
        if (currentQuestion === questions.length - 1) {
            await completeTest();
            return;
        }
        
        currentQuestion++;
    } else if (direction === 'prev' && currentQuestion > 0) {
        currentQuestion--;
    }

    updateQuestion();
}

function updateQuestion() {
    const questionContainer = document.getElementById('question-container');
    questionContainer.innerHTML = '';
    questionContainer.appendChild(createQuestionElement(questions[currentQuestion]));

    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');

    prevButton.style.display = currentQuestion > 0 ? 'block' : 'none';
    nextButton.textContent = currentQuestion === questions.length - 1 ? 'Finalizar' : 'Siguiente';

    updateProgressBar();
}

// Event Listeners
document.getElementById('prevButton').addEventListener('click', () => handleNavigation('prev'));
document.getElementById('nextButton').addEventListener('click', () => handleNavigation('next'));

// Inicialización
window.addEventListener('load', () => {
    const userId = localStorage.getItem('userId');
    if (!userId) {
        window.location.replace('/register');
        return;
    }
    updateQuestion();
});