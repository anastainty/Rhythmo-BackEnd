CREATE TABLE Users (
    user_id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(255) NOT NULL,
    email NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(MAX) NOT NULL,
    avatar_path NVARCHAR(MAX),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_Users_username ON Users (username);
CREATE INDEX idx_Users_email ON Users (email);

CREATE TABLE Artists (
    artist_id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(255) NOT NULL,
    bio TEXT,
    avatar_path NVARCHAR(MAX),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_Artists_name ON Artists (name);

CREATE TABLE Genres (
    genre_id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(255) NOT NULL
);

CREATE INDEX idx_Genres_name ON Genres (name);

CREATE TABLE Albums (
    album_id INT PRIMARY KEY IDENTITY(1,1),
    title NVARCHAR(255) NOT NULL,
    artist_id INT,
    release_date DATE,
    duration TIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_Albums_title ON Albums (title);

CREATE TABLE Tracks (
    track_id INT PRIMARY KEY IDENTITY(1,1),
    title NVARCHAR(255) NOT NULL,
    album_id INT,
    genre_id INT,
    duration TIME,
    file_path NVARCHAR(MAX),
    release_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
    ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE INDEX idx_Tracks_title ON Tracks (title);

CREATE TABLE Playlists (
    playlist_id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(255) NOT NULL,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX idx_Playlists_name ON Playlists (name);

CREATE TABLE Playlist_Tracks (
    playlist_track_id INT PRIMARY KEY IDENTITY(1,1),
    playlist_id INT,
    track_id INT,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Listening_History (
    listening_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT,
    track_id INT,
    listened_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);