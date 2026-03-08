import sys
import asyncio
import random
import time
import csv
import flet as ft

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def main(page: ft.Page):
    page.title = "SORTEIO NUMÉRICO v3.0"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "black"

    numeros_sorteados = []
    todos_numeros_sorteados = []
    min_num = 100
    max_num = 400

    async def generate_numbers(e):
        feedback_text.value = "Sorteando..."
        page.update()

        await asyncio.sleep(2)

        numbers = sorted(random.sample(range(min_num, max_num + 1), 1))
        numeros_sorteados.insert(0, numbers[0])
        todos_numeros_sorteados.append(numbers[0])

        if len(numeros_sorteados) > 10:
            numeros_sorteados.pop()

        atualizar_quadro()

        txt_number.content = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        value=str(number),
                        size=260,
                        color="white",
                        weight=ft.FontWeight.BOLD,
                    ),
                    width=470,
                    height=500,
                    bgcolor="green",
                    border_radius=25,
                    alignment=ft.alignment.center,
                )
                for number in numbers
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        feedback_text.value = f"O ganhador é o número {numbers[0]}!"
        salvar_resultados()
        page.update()
        animar_quadro()

    def clear_numbers(e):
        feedback_text.value = "Limpando resultado..."
        page.update()
        txt_number.content = None
        feedback_text.value = " "
        page.update()

    def clear_quadro(e):
        feedback_text.value = "Limpando quadro de resultados..."
        page.update()
        numeros_sorteados.clear()
        todos_numeros_sorteados.clear()
        atualizar_quadro()
        limpar_arquivo()
        feedback_text.value = " "
        page.update()

    def atualizar_quadro():
        quadro_numeros.content = ft.Column(
            controls=[
                ft.Text(value=str(num), size=48, color="white")
                for num in numeros_sorteados
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        page.update()

    def salvar_resultados():
        with open("resultados.txt", "w", encoding="utf-8") as file:
            for num in todos_numeros_sorteados:
                file.write(f"{num}\n")

    def limpar_arquivo():
        with open("resultados.txt", "w", encoding="utf-8") as file:
            file.write("")

    def exportar_resultados(e):
        with open("resultados.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Número Sorteado"])
            for num in todos_numeros_sorteados:
                writer.writerow([num])

        feedback_text.value = "Resultados exportados com sucesso!"
        page.update()

    def atualizar_intervalo(e):
        nonlocal min_num, max_num
        try:
            novo_min = int(min_input.value)
            novo_max = int(max_input.value)

            if novo_min >= novo_max:
                feedback_text.value = "Erro: mínimo deve ser menor que o máximo."
            else:
                min_num = novo_min
                max_num = novo_max
                feedback_text.value = f"Intervalo atualizado para {min_num} - {max_num}"
        except ValueError:
            feedback_text.value = "Digite apenas números inteiros."

        page.update()

    def animar_quadro():
        txt_number.scale = 1.1
        txt_number.update()
        time.sleep(0.5)
        txt_number.scale = 1.0
        txt_number.update()

    title = ft.Text(
        value="SORTEIO NUMÉRICO",
        size=64,
        color="white",
        weight=ft.FontWeight.BOLD,
    )

    texto_sorteados = ft.Text(
        value="JÁ SORTEADOS",
        size=18,
        color="white",
        weight=ft.FontWeight.BOLD,
    )

    feedback_text = ft.Text(value="", size=28, color="blue")

    txt_number = ft.Container(
        content=None,
        width=500,
        height=490,
        bgcolor="white",
        alignment=ft.alignment.center,
        border=ft.border.all(6, "green"),
        border_radius=25,
        padding=10,
        animate_scale=ft.Animation(
            duration=500,
            curve=ft.AnimationCurve.EASE_IN_OUT,
        ),
    )

    quadro_numeros = ft.Container(
        content=None,
        width=190,
        height=485,
        bgcolor="grey",
        border_radius=25,
        border=ft.border.all(6, "orange"),
        padding=10,
        alignment=ft.alignment.center,
    )

    btn_generate = ft.ElevatedButton(
        text="SORTEAR",
        on_click=generate_numbers,
        width=200,
        height=50,
        style=ft.ButtonStyle(
            color="white",
            bgcolor="green",
            text_style=ft.TextStyle(size=20),
        ),
    )

    btn_clear_quadro = ft.ElevatedButton(
        text="LIMPAR RESULTADOS",
        on_click=clear_quadro,
        width=200,
        height=50,
        style=ft.ButtonStyle(
            color="white",
            bgcolor="orange",
            text_style=ft.TextStyle(size=18),
        ),
    )

    btn_clear = ft.ElevatedButton(
        text="LIMPAR SORTEIO",
        on_click=clear_numbers,
        width=220,
        height=50,
        style=ft.ButtonStyle(
            color="white",
            bgcolor="red",
            text_style=ft.TextStyle(size=20),
        ),
    )

    btn_export = ft.ElevatedButton(
        text="EXPORTAR RESULTADOS",
        on_click=exportar_resultados,
        width=220,
        height=50,
        style=ft.ButtonStyle(
            color="white",
            bgcolor="blue",
            text_style=ft.TextStyle(size=18),
        ),
    )

    min_input = ft.TextField(label="Número Mínimo", value=str(min_num), width=220)
    max_input = ft.TextField(label="Número Máximo", value=str(max_num), width=220)

    btn_update_interval = ft.ElevatedButton(
        text="ATUALIZAR INTERVALO",
        on_click=atualizar_intervalo,
        width=220,
        height=50,
        style=ft.ButtonStyle(
            color="white",
            bgcolor="purple",
            text_style=ft.TextStyle(size=18),
        ),
    )

    container = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        texto_sorteados,
                        quadro_numeros,
                        btn_clear_quadro,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        feedback_text,
                        txt_number,
                        btn_generate,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        btn_clear,
                        btn_export,
                        min_input,
                        max_input,
                        btn_update_interval,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
    )

    page.add(ft.Container(content=title, alignment=ft.alignment.center))
    page.add(container)


ft.app(target=main)