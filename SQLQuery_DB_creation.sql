CREATE TABLE Users (
    user_id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar_path VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Artists (
    artist_id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    avatar_path VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Albums (
    album_id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(255) NOT NULL,
    artist_id INT,
    release_date DATE,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

CREATE TABLE Genres (
    genre_id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Tracks (
    track_id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(255) NOT NULL,
    album_id INT,
    genre_id INT,
    duration TIME,
    file_path VARCHAR(255),
    FOREIGN KEY (album_id) REFERENCES Albums(album_id),
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);

CREATE TABLE Playlists (
    playlist_id INT PRIMARY KEY IDENTITY(1,1),
    name VARCHAR(255) NOT NULL,
    user_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Playlist_Tracks (
    playlist_track_id INT PRIMARY KEY IDENTITY(1,1),
    playlist_id INT,
    track_id INT,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id),
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id)
);

CREATE TABLE Listening_History (
    listening_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT,
    track_id INT,
    listened_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id)
);

ALTER TABLE Albums
ADD CONSTRAINT FK_Albums_Artists
FOREIGN KEY (artist_id) REFERENCES Artists(artist_id);

ALTER TABLE Tracks
ADD CONSTRAINT FK_Tracks_Albums
FOREIGN KEY (album_id) REFERENCES Albums(album_id);

ALTER TABLE Playlists
ADD CONSTRAINT FK_Playlists_Users
FOREIGN KEY (user_id) REFERENCES Users(user_id);

ALTER TABLE Playlist_Tracks
ADD CONSTRAINT FK_PlaylistTracks_Playlists
FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id);

ALTER TABLE Playlist_Tracks
ADD CONSTRAINT FK_PlaylistTracks_Tracks
FOREIGN KEY (track_id) REFERENCES Tracks(track_id);

ALTER TABLE Listening_History
ADD CONSTRAINT FK_ListeningHistory_Users
FOREIGN KEY (user_id) REFERENCES Users(user_id);

ALTER TABLE Listening_History
ADD CONSTRAINT FK_ListeningHistory_Tracks
FOREIGN KEY (track_id) REFERENCES Tracks(track_id);

CREATE TABLE Profiles (
    profile_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT UNIQUE,
    additional_info TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
