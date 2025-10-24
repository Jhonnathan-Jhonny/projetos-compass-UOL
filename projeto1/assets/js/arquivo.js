import { Users } from './factory/userFactory.js';

let editIndex = -1;

document.addEventListener("DOMContentLoaded", () => {
    LoadUsers();
    document.getElementById("salvar").addEventListener("click", SaveUser);
    document.getElementById("cancelar").addEventListener("click", CancelAction);
    document.querySelector("#userTable tbody").addEventListener("click", function (e) {
        if (e.target && e.target.matches("button.btn-secondary")) {
            const index = e.target.dataset.index;
            DeleteUser(index);
        }   

        if (e.target && e.target.matches("button.btn-primary")) {
            const index = e.target.dataset.index;
            EditUser(index);
        }
    });
});

function CancelAction() {
    document.getElementById("formUser").reset();
    editIndex = -1;
}

function SaveUser() {
    let name = document.getElementById("name").value;
    let dateBirthRaw = document.getElementById("dateBirth").value; // formato: "2003-07-17"
    let telephone = document.getElementById("telephone").value;
    let email = document.getElementById("email").value;

    if (!name || !dateBirthRaw || !telephone || !email) {
        alert("Preencha todos os campos!");
        return;
    }

    const [year, month, day] = dateBirthRaw.split("-");
    let dateBirth = `${day}/${month}/${year}`; // monta manualmente

    telephone = formatPhoneNumber(telephone);
    let users = JSON.parse(localStorage.getItem("users")) || [];
    let user = new Users(name, dateBirth, telephone, email);

    if (editIndex === -1) {
        users.push(user);
    } else {
        users[editIndex] = user;
        editIndex = -1;
    }

    localStorage.setItem("users", JSON.stringify(users));
    LoadUsers();
    document.getElementById("formUser").reset();
}

function LoadUsers() {
    let users = JSON.parse(localStorage.getItem("users")) || [];
    let tbody = document.querySelector("#userTable tbody");
    tbody.innerHTML = "";

    users.forEach((user, index) => {
        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${user.name}</td>
            <td>${user.dateBirth}</td>
            <td>${user.telephone}</td>
            <td>${user.email}</td>
            <td>
                <button data-index="${index}" class="btn-secondary">Excluir</button>
                <button data-index="${index}" class="btn-primary">Editar</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function DeleteUser(index) {
    let users = JSON.parse(localStorage.getItem("users")) || [];
    if (!confirm("Tem certeza que deseja excluir este usuário?")) return;

    users.splice(index, 1);
    localStorage.setItem("users", JSON.stringify(users));
    LoadUsers();
}

function EditUser(index) {
    let users = JSON.parse(localStorage.getItem("users")) || [];
    let user = users[index];

    document.getElementById("name").value = user.name;
    document.getElementById("dateBirth").value = formatDateForInput(user.dateBirth);
    document.getElementById("telephone").value = user.telephone;
    document.getElementById("email").value = user.email;

    editIndex = index;
}

function formatPhoneNumber(phone) {
    phone = phone.replace(/\D/g, "");
    if (phone.length === 11) {
        return phone.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
    } else if (phone.length === 10) {
        return phone.replace(/(\d{2})(\d{4})(\d{4})/, "($1) $2-$3");
    }
    return phone;
}

function formatDateForInput(dateStr) {
    const [day, month, year] = dateStr.split('/');
    return `${year}-${month}-${day}`;
}
