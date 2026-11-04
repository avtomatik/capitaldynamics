from matplotlib.figure import Figure


def finish_axis(axis, *, title: str, xlabel: str, ylabel: str) -> None:
    axis.set_title(title)
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    axis.grid(True, alpha=0.35)


def add_reference_year(
    title: str, base_year: int, first_year: int, last_year: int
) -> str:
    return f"{title}, {base_year} = 100, {first_year}–{last_year}"


def close_figures(figures: dict[str, Figure]) -> None:
    import matplotlib.pyplot as plt

    for figure in figures.values():
        plt.close(figure)
