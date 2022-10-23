with open("input.txt", "r") as f_in:
    with open("output.txt", "w") as f_out:
        f_out.writelines(
            map(
                lambda x: " ".join(x.replace("\n", "").split(" ")[::2]) + "\n",
                f_in.readlines(),
            )
        )
