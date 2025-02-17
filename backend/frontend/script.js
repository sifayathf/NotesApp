const foldersDiv = document.getElementById("folders");
const filesDiv = document.getElementById("files");
const contentDiv = document.getElementById("content");

async function fetchFolders() {
    const response = await fetch("http://localhost:8000/folders/");
    const folders = await response.json();
    foldersDiv.innerHTML = folders.map(folder => `
        <div onclick="fetchFiles(${folder.id})">${folder.name}</div>
    `).join("");
}

async function fetchFiles(folderId) {
    const response = await fetch(`http://localhost:8000/files/?folder_id=${folderId}`);
    const files = await response.json();
    filesDiv.innerHTML = files.map(file => `
        <div onclick="fetchContent(${file.id})">${file.name}</div>
    `).join("");
}

async function fetchContent(fileId) {
    const response = await fetch(`http://localhost:8000/files/${fileId}`);
    const file = await response.json();
    contentDiv.innerHTML = file.content;
}

// Initial fetch for folders
fetchFolders();