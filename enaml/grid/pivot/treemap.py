import pandas
from collections import defaultdict
from enaml.qt.qt.QtCore import Qt, QRect
from enaml.qt.qt.QtGui import (
    QWidget, QPainter, QColor, QSizePolicy, QFontMetrics
    )

from .pandas_pivot import AggregationNode, MarginNode


class TreemapView(QWidget):

    #: Render the tree map in classic style
    ClassicStyle = 0

    #: Render the tree map in cluster style
    ClusterStyle = 1

    def __init__(self, parent):
        super(TreemapView, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._rect_cache = defaultdict(list)
        self._depth = 0
        self._engine = None

        self._style = TreemapView.ClassicStyle

        font = self.font()
        font.setPointSize(8)
        fm = QFontMetrics(font)
        small_spacing = fm.lineSpacing()
        self._line_heights = defaultdict(lambda: (font, small_spacing))

        font = self.font()
        font.setPointSize(11)
        font.setBold(True)
        fm = QFontMetrics(font)
        spacing = fm.lineSpacing()
        self._line_heights[0] = (font, spacing)
        self._line_heights[1] = (font, spacing)

        # XXX This is a hack
        from chaco.api import RdBu, DataRange1D

        self._cm = cm = RdBu(range=DataRange1D())
        cm.range.low = -0.1
        cm.range.high = 0.1

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def engine(self):
        """ Get the pivot engine used by the widget

        Returns
        -------
        result : PivotEngine
            The tabular engine being viewed by the widget

        """
        return self._engine

    def setEngine(self, engine):
        """ Set the engine being viewed by the widget

        Parameters
        ----------
        engine : TabularModel
            The engine to be viewed by the widget

        """
        self._engine = engine
        self._depth = engine.max_depth
        self._update()

    def style(self):
        """ Get the style of the treemap

        """
        return self._style

    def setStyle(self, style):
        """ Set the style of the treemap between classic and clustered
        style

        """
        valid = (TreemapView.ClassicStyle, TreemapView.ClusterStyle)
        assert style in valid
        self._style = style
        self._update()

    def setDepth(self, depth):
        self._depth = depth
        self.update()

    def resizeEvent(self, event):
        self._update()
        super(TreemapView, self).resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)

        cell = QColor(152, 186, 210)
        top_border = cell.lighter(110)
        bottom_border = cell.darker(200)

        render_depth = self._depth

        _, top_level_height = self._line_heights[0]

        if self._style == TreemapView.ClassicStyle:
            depths = range(render_depth, 0, -1)
        else:
            depths = range(0, render_depth+1)

        for depth in depths:
            font, spacing = self._line_heights[depth]
            fm = QFontMetrics(font)
            char_width = fm.averageCharWidth()*2

            for groups in self._rect_cache[depth]:
                for i, (name, rect, color) in enumerate(groups):
                    if (self._style == TreemapView.ClusterStyle or
                        depth == render_depth):
                        cell = QColor(*(color*255))
                        painter.fillRect(rect, cell)

                        top_border = cell.lighter(130)
                        bottom_border = cell.darker(130)
                        text_pen = cell.darker()
                        painter.setPen(bottom_border)
                        painter.drawPolyline([rect.bottomLeft(), rect.bottomRight(),
                                              rect.topRight()])
                        painter.setPen(top_border)
                        painter.drawPolyline([rect.topRight(), rect.topLeft(),
                                              rect.bottomLeft()])

                    else:
                        text_pen = Qt.black
                        painter.setPen(text_pen)
                        painter.drawRect(rect)

                    rect = rect.adjusted(3,2,-5,0)
                    if (rect.width() > char_width and
                        (self._style == TreemapView.ClusterStyle or
                         depth in (1, render_depth))):
                        if depth == 1:
                            painter.setPen(Qt.black)
                            painter.setFont(font)
                        else:
                            painter.setPen(text_pen)
                            painter.setFont(font)
                            if i == 0 and self._style == TreemapView.ClassicStyle:
                                rect.adjust(0, top_level_height, 0, 0)
                        text = str(name)
                        painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop, text)

    def _update(self):
        # Recompute layouts
        self.layout()
        self.update()

    def layout(self):
        rect = self.rect().adjusted(1,1,-1,-1)
        aggregate = self._engine.aggregates
        self._rect_cache = defaultdict(list)
        self.squarifyLayout(rect, aggregate)

    def squarifyLayout(self, bounds, aggregates, depth=1, index=tuple()):
        column, aggfunc = aggregates[0]
        pt = self._engine._get_pivot_table(aggregates[0], depth, 0).sort(column, ascending=False)[column]

        pt2 = self._engine._get_pivot_table(aggregates[1], depth, 0)[aggregates[1][0]]

        if isinstance(pt.index, pandas.MultiIndex):
            # XXX WTF the multiindex isn't working properly
            # for a Series
            for i in index:
                pt = pt.ix[i]
                pt2 = pt2.ix[i]

        x, y, w, h = bounds.x(), bounds.y(), bounds.width(), bounds.height()
        rects = self._layout(pt, x, y, w, h)

        self._rect_cache[depth].append(zip(pt.index, rects, self._cm.map_screen(pt2.ix[pt.index])))

        if depth >= self._engine.max_depth:
            return

        for idx, rect in zip(pt.index, rects):
            # Account for text
            if self._style == TreemapView.ClusterStyle:
                _, line_height = self._line_heights[depth]
                rect = rect.adjusted(5, line_height+6, -5, -5)
            self.squarifyLayout(rect, aggregates, depth+1, index+(idx,))

    def _layout(self, pt, x, y, w, h):
        size = len(pt)

        if size == 0: return []

        if (size < 2):
            return self._slice_layout(pt, x, y, w, h)

        total = pt.sum()

        mid = 0
        a = pt.irow(0) / total
        b = a

        if (w < h):
            while (mid < size):
                aspect = self.normAspect(h, w, a, b)
                q = pt.irow(mid) / total

                if self.normAspect(h,w,a,b+q) > aspect:
                    break

                mid += 1
                b += q

            rects = self._slice_layout(pt[:mid+1], x, y, w, round(h*b))
            return rects + self._layout(pt[mid+1:], x, y+round(h*b),w,round(h*(1-b)))
        else:
            while (mid < size):
                aspect = self.normAspect(w,h,a,b)
                q = pt.irow(mid) / total

                if self.normAspect(w,h,a,b+q) > aspect:
                    break

                mid += 1
                b += q

            rects = self._slice_layout(pt[:mid+1], x, y, round(w*b), h)
            return rects + self._layout(pt[mid+1:], x+round(w*b), y, round(w*(1-b)),h)

    def normAspect(self, big, small, a, b):
        x = (big * b) / (small * a / b)
        if x < 1: return 1/x
        else: return x

    def _slice_layout(self, pt, x, y, width, height):
        factors = pt / pt.sum()
        accum = pandas.np.zeros(len(factors))
        accum[1:] = factors[:-1].cumsum()

        if width <= height:
            rects = [QRect(x, y+round(height*a), width, round(height*f)) for f, a in zip(factors, accum)]
        else:
            rects = [QRect(x + round(width*a), y, round(width*f), height) for f, a in zip(factors, accum)]

        return rects


def treemap_view(engine, view_class=TreemapView, parent = None):
    """ Return a TreemapView configured to display a pandas engine
    """

    view = view_class(parent)
    view.setEngine(engine)
    return view

