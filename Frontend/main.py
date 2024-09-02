from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty
from kivymd.uix.tab import MDTabsBase
from kivy.core.window import Window

import requests

CATEGORIES = ["Pasta", "Breakfast", "Seafood", "Dessert", "Vegetarian", "Starter"]

# Window.size = (1080/2, 2082/2)
Builder.load_file("app.kv")

class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class HomeScreen(Screen):
    pass

class AccountScreen(Screen):
    username = StringProperty("John Doe")
    email = StringProperty("johndoe@example.com")
    phone = StringProperty("+1234567890")
    bio = StringProperty("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum vestibulum.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def edit_profile(self):
        # Functionality to edit profile
        pass

    def logout(self):
        # Functionality to logout
        pass

class ProfileScreen(Screen):
    pass


class SearchResultsScreen(Screen):
    pass


class CategoriesScreen(Screen):
    app = None

    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.app = app
        self.current_category = ""

        for category in CATEGORIES:
            self.ids.category_tabs.add_widget(Tab(title=category))

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """
        Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        """
        self.sm = ScreenManager(transition=NoTransition())
        self.current_category = tab_text
        self.ids.categories_results_grid.clear_widgets()
        self.ids.categories_results_grid.add_widget(CenteredSpinner())
        self.ids.categories_results_grid.height = (
            self.ids.categories_results_grid.minimum_height
        )
        self.ids.categories_results_label.text = f"Loading food items for {tab_text}..."

        UrlRequest(
            f"http://127.0.0.1:5000/meals/category/{tab_text}",
            self.show_category_results,
            on_error=self.on_error,
            on_failure=self.on_error,
            timeout=10,  
            verify=False,
        )

            
    def view_category(self, category_title):
        self.ids.category_tabs.switch_tab(
            search_by="property title", name_tab=category_title
        )

    def show_category_results(self, req, result):
        category_results = result["meals"]

        self.ids.categories_results_grid.clear_widgets()
        self.ids.categories_results_label.text = f'{len(category_results)} search result{"s" if len(category_results) > 1 else ""} for "{self.current_category}"'

        for category_result in category_results:
            self.ids.categories_results_grid.add_widget(
                ItemMedium(
                    source=category_result["strMealThumb"],
                    title=f"[size={int(self.app.scale(11))}][color=#ffffff][b] {category_result['strMeal']}[/b][/color][/size]",
                    category=f"[size=10][color=#808080][b]{self.current_category}[/b][/color][/size]",
                    item_id=category_result["idMeal"],
                    from_screen="categories",
                )
            )

        num_results_row = len(category_results) / 2
        if len(category_result) == 1:
            num_results_row = 1
        if num_results_row % 2 == 1:
            num_results_row += 0.5
        self.ids.categories_results_grid.height = self.app.scale(num_results_row * 170)

    def on_error(self, request, result):
        self.ids.categories_results_grid.clear_widgets()
        self.sm.error = ErrorScreen(name= 'error')

        self.ids.categories_results_grid.cols = 1
        self.ids.categories_results_grid.padding = [self.app.scale(30), self.app.scale(100)]
        self.ids.categories_results_grid.add_widget(self.sm.error)

class LoadingScreen(Screen):
    pass

class ErrorScreen(Screen):
    pass

class NoResults(RelativeLayout):
    pass


class CenteredSpinner(RelativeLayout):
    pass


class ItemMedium(RelativeLayout):
    source = StringProperty("")
    title = StringProperty("")
    category = StringProperty("")
    item_id = StringProperty("")
    from_screen = StringProperty("")



class ItemDetailScreen(Screen):
    img = StringProperty("")
    title = StringProperty("")
    category = StringProperty("")
    area = StringProperty("")
    canteen = StringProperty("")
    price = StringProperty("")
    description = StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.title = kw["title"]
        self.img = kw["img"]
        self.category = kw["category"]
        self.area = kw["area"]
        self.canteen = kw["canteen"]
        self.price = kw["price"]


class CanteenEase(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.back_screen = "home"
        self.search_value = ""
        self.window_width = Window.size[0]
        self.window_height = Window.size[1]
        self.scale_by = (self.window_width * self.window_height)/520000
        self.scale_by += 0.35

    def open_account(self):
        self.sm.current = "account"

    def scale(self, value):
        return value * 2.5

    def load_item_detail(self, item_id, from_screen):
        if from_screen != "item_detail":
            self.back_screen = from_screen
        UrlRequest(
            f"http://127.0.0.1:5000/meal/{item_id}",
            self.show_item_detail,
            on_error=self.on_error,
            on_failure=self.on_error,
            timeout=10,  
            verify=False,
        )

        self.sm.current = "loading"

    def show_item_detail(self, req, result):
        id = result['idMeal']
        if "error" in result:
            # Handle the error (e.g., show a popup or navigate back)
            self.sm.current = self.back_screen
        else:
            item_detail_screen = self.sm.get_screen('item_detail')
            item_detail_screen.img = result['strMealThumb']
            item_detail_screen.title = result['strMeal']
            item_detail_screen.category = result['strCategory']
            item_detail_screen.area = result['strArea']
            item_detail_screen.canteen = result['strCanteen']
            item_detail_screen.price = result['strPrice']
            item_detail_screen.description = result['strDescription']

            def show_restaurant_items(req, result):
                search_results = result["meals"]

                if search_results is None:
                    self.item_detail.ids.canteen_items_grid.add_widget(NoResults())
                    self.sm.current = "item_detail"
                    self.item_detail.ids.canteen_items_grid.height = (
                        self.item_detail.ids.canteen_items_grid.minimum_height
                    )
                    return

                for search_result in search_results:
                    if search_result["idMeal"] != id:
                        self.item_detail.ids.canteen_items_grid.add_widget(
                            ItemMedium(
                                source=search_result["strMealThumb"],
                                title=f"[size={int(self.scale(11))}][color=#ffffff][b] {search_result['strMeal']}[/b][/color][/size]",
                                category=f"[size=10][color=#808080][b]{search_result['strCategory']}[/b][/color][/size]",
                                item_id=search_result["idMeal"],
                                from_screen="item_detail",
                            )
                        )
                if len(search_results) > 1:
                    self.item_detail.ids.canteen_items_grid.height = self.scale(
                        len(search_results) * 100
                    )
                else:
                    self.item_detail.ids.canteen_items_grid.height = self.scale(50)
            self.item_detail.ids.canteen_items_grid.clear_widgets()

            search_value_encoded = requests.utils.quote(result['strCanteen'])
    
            UrlRequest(
                f"http://127.0.0.1:5000/search?query={search_value_encoded}",
                show_restaurant_items,
                on_error=self.on_error,
                on_failure=self.on_error,
                timeout=10,  
                verify=False,
            )

            self.sm.current = "loading"

            self.sm.current = 'item_detail'

    def load_profile(self):
        self.sm.current = "profile"


    def item_detail_back(self):
        self.sm.current = self.back_screen

    def load_search_results(self, root):
        self.search_value = root.ids.search_bar.text
        search_value_encoded = requests.utils.quote(self.search_value)
    
        UrlRequest(
            f"http://127.0.0.1:5000/search?query={search_value_encoded}",
            self.show_search_results,
            on_error=self.on_error,
            on_failure=self.on_error,
            timeout=10,  
            verify=False,
        )
        self.sm.current = "loading"

    def on_error(self, request, result):
        self.search_results.ids.search_results_grid.clear_widgets()
        self.sm.error = ErrorScreen(name= 'error')
        self.search_results.ids.search_results_label.text = ""
        self.search_results.ids.search_results_container.add_widget(self.sm.error)
        self.sm.current = "search_results"
        self.search_results.ids.search_results_container.height = (
            self.search_results.ids.search_results_container.minimum_height
        )
        return

    def show_search_results(self, req, result):
        search_results = result["meals"]
        self.sm.remove_widget(self.search_results)
        self.search_results = SearchResultsScreen(name="search_results")
        self.sm.add_widget(self.search_results)

        self.search_results.ids.search_bar.text = self.search_value
        self.search_results.ids.search_results_grid.clear_widgets()

        if search_results is None:
            self.search_results.ids.search_results_label.text = ""
            self.search_results.ids.search_results_container.add_widget(NoResults())
            self.sm.current = "search_results"
            self.search_results.ids.search_results_container.height = (
                self.search_results.ids.search_results_container.minimum_height
            )
            return

        for search_result in search_results:
            self.search_results.ids.search_results_grid.add_widget(
                ItemMedium(
                    source=search_result["strMealThumb"],
                    title=f"[size={int(self.scale(11))}][color=#ffffff][b] {search_result['strMeal']}[/b][/color][/size]",
                    category=f"[size=10][color=#808080][b]{search_result['strCategory']}[/b][/color][/size]",
                    item_id=search_result["idMeal"],
                    from_screen="search_results",
                )
            )
        num_results_row = len(search_results) / 2
        if len(search_results) == 1:
            num_results_row = 1
        if num_results_row % 2 == 1:
            num_results_row += 0.5
        self.search_results.ids.search_results_grid.height = self.scale(
            num_results_row * 170
        )
        self.search_results.ids.search_results_label.text = f'{len(search_results)} search result{"s" if len(search_results) > 1 else ""} for "{self.search_value}"'
        self.sm.current = "search_results"

    def view_category(self, category_title):
        self.sm.current = "categories"
        self.categories_screen.view_category(category_title=category_title)

    def build(self):
        self.theme_cls.primary_palette = "Brown"
        self.sm = ScreenManager(transition=NoTransition())

        self.home = HomeScreen(name="home")
        self.sm.add_widget(self.home)
        self.sm.add_widget(LoadingScreen(name="loading"))
        self.item_detail = ItemDetailScreen(
            name="item_detail", img="", title="", category="", area="", canteen="", price="", description=""
        )
        self.sm.add_widget(self.item_detail)
        self.search_results = SearchResultsScreen(name="search_results")
        self.sm.add_widget(self.search_results)
        self.categories_screen = CategoriesScreen(self, name="categories")
        self.sm.add_widget(self.categories_screen)
        self.account_screen = AccountScreen(name="account")
        self.sm.add_widget(self.account_screen)
        self.sm.profile = ProfileScreen(name="profile")
        self.sm.add_widget(self.sm.profile)
        return self.sm
    


if __name__ == "__main__":
    CanteenEase().run()
