import sublime

class PhpDependencies:

    """Get imported class from a view"""
    def get_imported_classes(self, view):
        return view.find_by_selector('meta.use.php meta.path.php support.class.php')

    """Get used classes in code"""
    def get_dependencies(self, view):

        # Get all dependencies
        classes = view.find_by_selector('support.class.php')
        extensions = view.find_by_selector('meta.path.php entity.other.inherited-class.php')

        # List of dependencies
        classes.reverse()
        dependencies = extensions + classes

        # Grab imported classes to filter them
        imported = self.get_imported_classes(view)

        return self.filter_duplicate_regions(dependencies, imported)

    """Include namespace"""
    def include_namespace(self, view, region):
        extended = sublime.Region(region.a - 1, region.b)
        string = view.substr(extended)

        if string[0] in [" ", "(", "[", "{"]:
            return region
        else:
            return self.include_namespace(view, extended)

    """Filter duplicate regions"""
    def filter_duplicate_regions(self, regions1, regions2):
        return [region for region in regions1 if region not in regions2]

    """Check if dependencies are imported"""
    def get_unimported(self, view, dependencies_r, imported_r):
        dependencies = list()
        imported = list()

        # Convert dependency regions to strings
        for dependency in dependencies_r:
            dependencies.append(view.substr(dependency))

        # Convert imported classes regions to strings
        for entity in imported_r:
            imported.append(view.substr(entity))

        # Calculate difference and get the regions
        diff = [dep for dep in dependencies if dep in imported]
        regions = [dep for dep in dependencies_r if view.substr(dep) not in diff]

        regions.reverse()

        return regions