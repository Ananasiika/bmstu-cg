#include "objects.h"

point_t point(double x, double y) {
    return point_t{std::vector<double>{x, y, 1}};
}

linear_figure_t create_line(point_t a, point_t b) {
    linear_figure_t res;
    res.edges.push_back(edge_t{a, b});
    return res;
}

object_t create_horse() {
    object_t res;

    res.linear_figures.push_back(create_line(point(121, 383), point(161, 365)));
    res.linear_figures.push_back(create_line(point(121, 383), point(148, 517)));
    res.linear_figures.push_back(create_line(point(143, 348), point(148, 517)));
    res.linear_figures.push_back(create_line(point(143, 348), point(240, 303)));
    res.linear_figures.push_back(create_line(point(156, 343), point(182, 453)));
    res.linear_figures.push_back(create_line(point(171, 513), point(182, 453)));
    res.linear_figures.push_back(create_line(point(171, 513), point(195, 527)));
    res.linear_figures.push_back(create_line(point(208, 606), point(195, 527)));
    res.linear_figures.push_back(create_line(point(208, 606), point(191, 606)));
    res.linear_figures.push_back(create_line(point(171, 513), point(191, 606)));
    res.linear_figures.push_back(create_line(point(245, 425), point(182, 453)));
    res.linear_figures.push_back(create_line(point(245, 425), point(195, 527)));
    res.linear_figures.push_back(create_line(point(245, 425), point(271, 314)));
    res.linear_figures.push_back(create_line(point(245, 425), point(392, 453)));
    res.linear_figures.push_back(create_line(point(240, 303), point(271, 314)));
    res.linear_figures.push_back(create_line(point(378, 319), point(271, 314)));
    res.linear_figures.push_back(create_line(point(378, 319), point(392, 453)));
    res.linear_figures.push_back(create_line(point(378, 319), point(474, 410)));
    res.linear_figures.push_back(create_line(point(378, 319), point(461, 257)));
    res.linear_figures.push_back(create_line(point(411, 515), point(392, 453)));
    res.linear_figures.push_back(create_line(point(411, 515), point(474, 410)));
    res.linear_figures.push_back(create_line(point(516, 246), point(461, 257)));
    res.linear_figures.push_back(create_line(point(516, 246), point(512, 318)));
    res.linear_figures.push_back(create_line(point(516, 246), point(554, 252)));
    res.linear_figures.push_back(create_line(point(516, 246), point(557, 228)));
    res.linear_figures.push_back(create_line(point(554, 252), point(557, 228)));
    res.linear_figures.push_back(create_line(point(473, 366), point(512, 318)));
    res.linear_figures.push_back(create_line(point(473, 366), point(474, 410)));
    res.linear_figures.push_back(create_line(point(590, 342), point(554, 252)));
    res.linear_figures.push_back(create_line(point(590, 342), point(573, 357)));
    res.linear_figures.push_back(create_line(point(512, 318), point(573, 357)));
    res.linear_figures.push_back(create_line(point(411, 515), point(418, 606)));
    res.linear_figures.push_back(create_line(point(432, 606), point(418, 606)));
    res.linear_figures.push_back(create_line(point(432, 606), point(444, 464)));

    res.center = point(350, 350);

    return res;
}

void draw_edge(edge_t e, QPainter &painter)
{
    int height = painter.device()->height();
    painter.drawLine(e.p1.cords[0], height - e.p1.cords[1], e.p2.cords[0], height - e.p2.cords[1]);
}

void draw_linear(linear_figure_t f, QPainter &painter)
{
    for (uint i = 0; i < f.edges.size(); ++i)
        draw_edge(f.edges[i], painter);
}

void draw_object(object_t o, QPainter &painter)
{
    for (uint i = 0; i < o.linear_figures.size(); ++i)
        draw_linear(o.linear_figures[i], painter);
}

point_t move_point(point_t p, double dx, double dy)
{
    std::vector<std::vector<double>> matrix;
    matrix.push_back(std::vector<double>{1, 0, 0});
    matrix.push_back(std::vector<double>{0, 1, 0});
    matrix.push_back(std::vector<double>{dx, dy, 1});
    return point_t{multiplication(p.cords, matrix)};
}

edge_t move_edge(edge_t e, double dx, double dy)
{
    return edge_t{move_point(e.p1, dx, dy), move_point(e.p2, dx, dy)};
}

linear_figure_t move_linear(linear_figure_t f, double dx, double dy)
{
    linear_figure_t res;

    for (uint i = 0; i < f.edges.size(); ++i)
        res.edges.push_back(move_edge(f.edges[i], dx, dy));

    return res;
}
object_t move_object(object_t o, double dx, double dy)
{
    object_t res;

    for (uint i = 0; i < o.linear_figures.size(); ++i)
        res.linear_figures.push_back(move_linear(o.linear_figures[i], dx, dy));

    res.center = move_point(o.center, dx, dy);
    return res;
}

point_t scale_point_c(point_t p, double kx, double ky)
{
    std::vector<std::vector<double>> matrix;
    matrix.push_back(std::vector<double>{kx, 0, 0});
    matrix.push_back(std::vector<double>{0, ky, 0});
    matrix.push_back(std::vector<double>{0, 0, 1});
    return point_t{multiplication(p.cords, matrix)};
}

point_t scale_point(point_t p, double kx, double ky, double xc, double yc)
{
    return move_point(scale_point_c(move_point(p, -xc, -yc), kx, ky), xc, yc);
}

edge_t scale_edge(edge_t e, double kx, double ky, double xc, double yc)
{
    edge_t res;
    res.p1 = scale_point(e.p1, kx, ky, xc, yc);
    res.p2 = scale_point(e.p2, kx, ky, xc, yc);
    return res;
}

linear_figure_t scale_linear(linear_figure_t f, double kx, double ky, double xc, double yc)
{
    linear_figure_t res;
    for (int i = 0; i < f.edges.size(); ++i)
        res.edges.push_back(scale_edge(f.edges[i], kx, ky, xc, yc));

    return res;
}

object_t scale_object(object_t o, double kx, double ky, double xc, double yc)
{
    object_t res;
    for (uint i = 0; i < o.linear_figures.size(); ++i)
        res.linear_figures.push_back(scale_linear(o.linear_figures[i], kx, ky, xc, yc));

    res.center = scale_point(o.center, kx, ky, xc, yc);
    return res;
}

point_t rotate_point_c(point_t p, double angle)
{
    std::vector<std::vector<double>> matrix;
    matrix.push_back(std::vector<double>{cos(angle), -sin(angle), 0});
    matrix.push_back(std::vector<double>{sin(angle), cos(angle), 0});
    matrix.push_back(std::vector<double>{0, 0, 1});
    return point_t{multiplication(p.cords, matrix)};
}

point_t rotate_point(point_t p, double angle, double xc, double yc)
{
    return move_point(rotate_point_c(move_point(p, -xc, -yc), angle), xc, yc);
}

edge_t rotate_edge(edge_t e, double angle, double xc, double yc)
{
    edge_t res;
    res.p1 = rotate_point(e.p1, angle, xc, yc);
    res.p2 = rotate_point(e.p2, angle, xc, yc);
    return res;
}

linear_figure_t rotate_linear(linear_figure_t f, double angle, double xc, double yc)
{
    linear_figure_t res;
    for (int i = 0; i < f.edges.size(); ++i)
        res.edges.push_back(rotate_edge(f.edges[i], angle, xc, yc));

    return res;
}

object_t rotate_object(object_t o, double angle, double xc, double yc)
{
    object_t res;
    for (uint i = 0; i < o.linear_figures.size(); ++i) {
        res.linear_figures.push_back(rotate_linear(o.linear_figures[i], angle, xc, yc));
    }

    res.center = rotate_point(o.center, angle, xc, yc);
    return res;
}
