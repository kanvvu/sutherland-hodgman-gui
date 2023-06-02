import PySimpleGUI as sg
import random
import copy
import math
from sutherland_hodgeman import sutherland_hodgeman, is_inside
from utils import Polygon


def draw_rect(cords, graph, rect_lines, linewidth=0.5, color="red"):
    p = [cords[0], (cords[1][0], cords[0][1]), cords[1],
         (cords[0][0], cords[1][1])]

    for i in range(len(p)):
        rect_lines.append(graph.draw_line(p[i], p[(i+1) % len(p)], "green", 1))


def main():

    sg.theme('Dark Blue 3')

    col = [[sg.Radio('Move canvas', 1, key='-MOVE-', enable_events=True)],
           [sg.Radio('Move object', 1, key='-MOVEO-', enable_events=True)],
           [sg.Radio('Make polygon', 1, key='-POLY-', enable_events=True)],
           [sg.Radio('Make clip rect', 1, key='-RECT-', enable_events=True)],
           [sg.Radio('Make clip ploygon', 1, key='-CPOLY-', enable_events=True)],
           [sg.B('CLIP', key='-CLIP-', enable_events=True)],
           [sg.B('CUT', key='-CUT-', enable_events=True)]]

    layout = [[sg.Graph(
        canvas_size=(500, 500),
        graph_bottom_left=(0, 500),
        graph_top_right=(500, 0),
        key="-GRAPH-",
        enable_events=True,
        motion_events=True,
        background_color='lightblue',
        drag_submits=True,
        right_click_menu=[
            [''], ['Finish', 'Clip', 'Clear', 'Remove polygon', 'Remove rect']]
    ), sg.Col(col, key='-COL-')]]

    window = sg.Window("sutherland-hodgeman algorithm", layout,
                       return_keyboard_events=True, finalize=True)

    graph = window["-GRAPH-"]

    poly = Polygon(graph, [], 3, "black")
    move_poly = False

    clip_poly = Polygon(graph, [], 3, "green")
    move_clip_poly = False

    rect = Polygon(graph, [], 2, "green")
    move_rect = False

    clip = Polygon(graph, [], 4, "red")
    move_clip = False

    dragging = False

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-GRAPH-':
            x, y = values["-GRAPH-"]

            if not dragging:
                dragging = True
                start_point = (x, y)
                drag_figures = graph.get_figures_at_location((x, y))

                move_clip_poly = False
                move_rect = False
                move_poly = False
                move_clip = False
                for fig in drag_figures:
                    for pol in clip_poly.lines:
                        if fig == pol:
                            move_clip_poly = True
                            break
                    for pol in rect.lines:
                        if fig == pol:
                            move_rect = True
                            break
                    for pol in poly.lines:
                        if fig == pol:
                            move_poly = True
                            break
                    for pol in clip.lines:
                        if fig == pol:
                            move_clip = True
                            break

                lastxy = (x, y)

                if values['-POLY-']:
                    if not poly.finished:
                        poly.add_point(x, y)

                if values['-CPOLY-']:
                    if not clip_poly.finished:
                        clip_poly.add_point(x, y)

                if values['-RECT-']:
                    if not rect.finished:
                        if len(rect.points) == 0:
                            rect.add_point(x, y)

                        if len(rect.points) == 4:
                            rect.earse(True)
                            p = [
                                rect.points[0], (x, rect.points[0][1]), (x, y), (rect.points[0][0], y)]
                            rect.add_points(p)

            delta_x, delta_y = x - lastxy[0], y - lastxy[1]
            lastxy = x, y

            if values['-MOVE-']:
                graph.move(delta_x, delta_y)
                clip_poly.move(delta_x, delta_y)
                poly.move(delta_x, delta_y)
                rect.move(delta_x, delta_y)

            if dragging and values['-MOVEO-']:
                if poly.finished or rect.finished or clip_poly.finished:
                    if move_poly:
                        poly.move(delta_x, delta_y)
                    if move_clip_poly:
                        clip_poly.move(delta_x, delta_y)
                        poly_cords = copy.deepcopy(clip_poly.points)
                    if move_rect:
                        rect.move(delta_x, delta_y)
                        poly_cords = copy.deepcopy(rect.points)

                    if clip.finished:
                        if not is_inside(poly_cords[2], poly_cords[0], poly_cords[1]):
                            poly_cords.reverse()
                        clip_points = sutherland_hodgeman(
                            poly.points, poly_cords)

                        clip.earse(True)
                        if len(clip_points) > 0:
                            clip.add_points(clip_points)
                else:
                    if move_clip:
                        clip.move(delta_x, delta_y)

        if event.endswith('+UP'):
            dragging = False

        if event == "-GRAPH-+MOVE":
            dragging = False

            x, y = values["-GRAPH-"]

            if not rect.finished:
                if len(rect.points) > 0:
                    rect.earse(False)
                    p = [rect.points[0], (x, rect.points[0][1]),
                         (x, y), (rect.points[0][0], y)]
                    rect.add_points(p)
                    rect.finished = False

            if not poly.finished:
                if len(poly.points) > 0:
                    if len(poly.lines) > 0:
                        poly.delete_figure(-1)
                    poly.add_point(x, y)

            if not clip_poly.finished:
                if len(clip_poly.points) > 0:
                    if len(clip_poly.lines) > 0:
                        clip_poly.delete_figure(-1)
                    clip_poly.add_point(x, y)

            if len(graph.get_figures_at_location((x, y))) == 0:
                graph.set_cursor(cursor='arrow')
            elif values['-MOVEO-']:
                graph.set_cursor(cursor='fleur')

        if event == '-CLIP-' or event == 'Clip' or event == 'w':
            if rect.finished:
                poly_cords = copy.deepcopy(rect.points)
            else:
                poly_cords = copy.deepcopy(clip_poly.points)

            if not is_inside(poly_cords[2], poly_cords[0], poly_cords[1]):
                poly_cords.reverse()

            clip_points = sutherland_hodgeman(poly.points, poly_cords)
            if len(clip_points) > 0:
                clip.add_points(clip_points)

        if event == '-CUT-':
            clip_poly.earse(False)
            clip_poly.points.clear()

            poly.earse(False)
            poly.points.clear()

            rect.earse(False)
            rect.points.clear()

        if event == 'Clear':
            clip_poly.earse(False)
            clip_poly.points.clear()

            poly.earse(False)
            poly.points.clear()

            rect.earse(False)
            rect.points.clear()

            clip.earse(False)
            clip.points.clear()

        if event == 'Finish':
            if values['-POLY-']:
                if not poly.finished:
                    if len(poly.points) > 3:
                        poly.delete_figure(-1)
                        poly.finish_polygon()

            if values['-CPOLY-']:
                if not clip_poly.finished:
                    if len(clip_poly.points) > 3:
                        clip_poly.delete_figure(-1)
                        clip_poly.finish_polygon()

        if event == 'Remove polygon':
            poly.earse(False)
            poly.points.clear()

        if event == 'Remove rect' or event == 'q':
            rect.earse(False)
            rect.points.clear()

            clip_poly.earse(False)
            clip_poly.points.clear()

            clip.earse(False)
            clip.points.clear()

    window.close()


main()
