import sys
if __name__ == "__main__":
    if sys.version_info.major != 3:
        print("This program must be executed using python 3.X You are currently using python " \
        +str(sys.version_info.major)+"."+str(sys.version_info.minor))
        sys.exit(0)
    print("Generating wav files from frequencies db...")
    import Utils.wav_create_notes_from_frequencies_db
    print("Done generating!")
    from UI.main_ui import MainUI
    app = MainUI()
    app.mainloop()
