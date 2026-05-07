"""
transit_data.py
Classes for storing and working with transit route delay data.
By: Sankalp Khira
"""


def _categorize_delay(delay: float) -> str:
    """Classify a delay value into a category string."""
    if delay <= 2:
        return "On Time"
    elif delay <= 5:
        return "Minor"
    elif delay <= 10:
        return "Moderate"
    else:
        return "Severe"


class TransitRoute:
    """Stores delay records for a single route."""

    def __init__(self, route_id: str):
        self.route_id = route_id
        self._delays = []              # list of float delays
        self._delay_categories = []    # corresponding category for each trip

    def add_record(self, delay: float):
        """Add a trip's delay to this route."""
        self._delays.append(delay)
        self._delay_categories.append(_categorize_delay(delay))

    @property
    def average_delay(self):
        if not self._delays:
            return 0.0
        return sum(self._delays) / len(self._delays)

    @property
    def max_delay(self):
        return max(self._delays) if self._delays else 0.0

    @property
    def delays(self):
        """Return a copy so outside code can't mess with the internal list."""
        return list(self._delays)

    @property
    def category_set(self):
        """Set of unique delay categories seen on this route."""
        return set(self._delay_categories)

    def category_breakdown(self):
        """Count trips per delay category — returns a dict."""
        counts = {}
        for c in self._delay_categories:
            counts[c] = counts.get(c, 0) + 1
        return counts

    # -- dunder methods --

    def __str__(self):
        return f"Route {self.route_id}: {len(self)} trips, avg delay {self.average_delay:.2f} min"

    def __len__(self):
        return len(self._delays)

    def __eq__(self, other):
        if not isinstance(other, TransitRoute):
            return NotImplemented
        return self.route_id == other.route_id

    def __hash__(self):
        return hash(self.route_id)

    def __getattr__(self, name):
        """Fallback for accessing unknown attributes — gives a clearer error."""
        raise AttributeError(f"TransitRoute has no attribute '{name}'")


class TransitNetwork:
    """
    Collection of TransitRoute objects.
    Composition relationship — a network *contains* routes.
    """

    def __init__(self):
        self._routes = {}   # dict mapping route_id -> TransitRoute

    def add_record(self, route_id: str, delay: float):
        """Add a trip record, creating the route if it doesn't exist yet."""
        if route_id not in self._routes:
            self._routes[route_id] = TransitRoute(route_id)
        self._routes[route_id].add_record(delay)

    def get_route(self, route_id: str):
        return self._routes.get(route_id)

    @property
    def route_ids(self):
        return set(self._routes.keys())

    @property
    def all_routes(self):
        return list(self._routes.values())

    def routes_above_threshold(self, threshold: float):
        """List comprehension — returns routes with avg delay above threshold."""
        return [r for r in self._routes.values() if r.average_delay > threshold]

    def delay_generator(self):
        """Generator that yields (route_id, delay) one at a time."""
        for route in self._routes.values():
            for d in route.delays:
                yield (route.route_id, d)

    # set operations on route delay-category data
    def common_categories(self, route_id_a: str, route_id_b: str):
        """Intersection of delay categories between two routes."""
        a = self._routes.get(route_id_a)
        b = self._routes.get(route_id_b)
        if a is None or b is None:
            return set()
        return a.category_set & b.category_set    # set intersection

    def all_delay_categories(self):
        """Union of delay categories across all routes."""
        result = set()
        for route in self._routes.values():
            result = result | route.category_set   # set union
        return result

    def unique_categories(self, route_id: str):
        """Delay categories seen ONLY on this route (set difference)."""
        route = self._routes.get(route_id)
        if route is None:
            return set()
        others = set()
        for rid, r in self._routes.items():
            if rid != route_id:
                others = others | r.category_set
        return route.category_set - others         # set difference

    def __len__(self):
        return len(self._routes)

    def __contains__(self, route_id: str):
        return route_id in self._routes

    def __iter__(self):
        return iter(self._routes.values())

    def __str__(self):
        return f"TransitNetwork: {len(self)} routes"


if __name__ == "__main__":
    # quick sanity check
    net = TransitNetwork()
    net.add_record("R1", 5.0)
    net.add_record("R1", 12.0)
    net.add_record("R2", 3.0)
    print(net)
    for r in net:
        print(r)
