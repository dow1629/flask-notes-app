async function loadNotes() {
    const status = document.getElementById("status");
    const notesList = document.getElementById("notes-list");

    status.textContent = "Loading notes...";

    try {
        const response = await fetch("/api/notes");

        if (!response.ok) {
            throw new Error("Failed to load notes.");
        }

        const data = await response.json();

        notesList.innerHTML = "";

        data.notes.forEach((note) => {
            const noteElement = document.createElement("div");
            
            noteElement.className = "note";
            noteElement.innerHTML = `
    <h3>${note.name}</h3>
    <p>${note.message}</p>
    <small>${note.category}</small>
    <button type="button" class="delete-button">Delete</button>
`;

const deleteButton = noteElement.querySelector(".delete-button");

deleteButton.addEventListener("click", async () => {
    await deleteNote(note.id);
});

notesList.appendChild(noteElement);
        });

        status.textContent = "";
    } catch (error) {
        status.textContent = error.message;
    }
}

loadNotes();


const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const status = document.getElementById("status");

    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    status.textContent = "Logging in...";

    try {
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Login failed.");
        }

        status.textContent = "Logged in successfully.";
        loginForm.reset();
    } catch (error) {
        status.textContent = error.message;
    }
});


const noteForm = document.getElementById("note-form");

noteForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const status = document.getElementById("status");

    const name = document.getElementById("name").value;
    const message = document.getElementById("message").value;
    const categoryId = Number(
        document.getElementById("category").value
    );

    status.textContent = "Adding note...";

    try {
        const response = await fetch("/api/notes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                message: message,
                category_id: categoryId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to add note.");
        }

        noteForm.reset();

        await loadNotes();

        status.textContent = "Note added successfully.";
    } catch (error) {
        status.textContent = error.message;
    }
});

async function deleteNote(noteId) {
    const status = document.getElementById("status");

    status.textContent = "Deleting note...";

    try {
        const response = await fetch(`/api/notes/${noteId}`, {
            method: "DELETE"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to delete note.");
        }

        await loadNotes();

        status.textContent = "Note deleted successfully.";
    } catch (error) {
        status.textContent = error.message;
    }
}