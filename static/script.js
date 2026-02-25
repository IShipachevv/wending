console.log("--- JS ЗАГРУЖЕН ---"); // Если видишь это в консоли - JS работает!

document.addEventListener('DOMContentLoaded', function() {
    // 1. Находим элементы
    const allergyCheck = document.getElementById('allergy-check');
    const allergyDetails = document.getElementById('allergy-details');
    const rsvpForm = document.getElementById('rsvpForm');

    // Проверка наличия элементов (для отладки)
    if (!allergyCheck || !allergyDetails) {
        console.error("ОШИБКА: Элементы аллергии не найдены! Проверь ID в HTML.");
    }

    // 2. Логика появления поля (Toggle)
    if (allergyCheck) {
        allergyCheck.addEventListener('change', function() {
            console.log("Галочка аллергии:", this.checked);
            if (this.checked) {
                allergyDetails.classList.remove('hidden');
            } else {
                allergyDetails.classList.add('hidden');
            }
        });
    }

    // 3. Отправка формы (чтобы не было GET-запроса в ссылке)
    if (rsvpForm) {
        rsvpForm.addEventListener('submit', async function(e) {
            e.preventDefault(); // ОСТАНАВЛИВАЕТ ПЕРЕЗАГРУЗКУ

            console.log("Начинаем отправку...");

            const alcohol = Array.from(document.querySelectorAll('input[name="alcohol"]:checked'))
                                 .map(el => el.value);

            const formData = {
                name: document.getElementById('name').value,
                phone: document.getElementById('phone').value,
                coming: document.querySelector('input[name="coming"]:checked').value,
                alcohol: alcohol,
                has_allergy: allergyCheck.checked,
                allergy_info: document.getElementById('allergy-text').value,
                wish: document.getElementById('wish') ? document.getElementById('wish').value : ""
            };

            try {
                const response = await fetch('/api/rsvp', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();
                if (result.success) {
                    alert("Спасибо! Ваш ответ записан.");
                    rsvpForm.reset();
                    allergyDetails.classList.add('hidden');
                }
            } catch (error) {
                console.error("Ошибка отправки:", error);
                alert("Произошла ошибка при связи с сервером.");
            }
        });
    }
});