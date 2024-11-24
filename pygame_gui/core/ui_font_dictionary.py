import os
import warnings

from typing import Dict, Union, Tuple, List, Optional

import pygame
from pygame_gui.core.interfaces.gui_font_interface import IGUIFontInterface
from pygame.font import match_font

from pygame_gui.core.interfaces.font_dictionary_interface import IUIFontDictionaryInterface
from pygame_gui.core.resource_loaders import IResourceLoader
from pygame_gui.core.utility import PackageResource
from pygame_gui.core.utility import FontResource


# TEMP hack
print("TEMP hack in ui_font_dictionary to use local folder font file path reference")

pkg_folder, _ = os.path.split(__file__)
src = os.path.dirname(os.path.abspath(__file__))

def fonts_path(*filepath):
    return os.path.join(os.path.join(pkg_folder, "..", "data"), *filepath)



class DefaultFontData:
    """
    Data class to wrap up all the data for a default font. Used now that we have multiple
    default fonts for different locales.
    """

    def __init__(self, size: int, name: str, style: str,
                 regular_file_name: str,
                 bold_file_name: str,
                 italic_file_name: str,
                 bold_italic_file_name: str,
                 script: str = 'Latn',
                 direction: int = pygame.DIRECTION_LTR):
        self.size = size
        self.name = name
        self.style = style
        self.script = script
        self.direction = direction
        self.idx = (self.name + '_' + self.style + '_' + 'aa_' + str(self.size))

        self.regular_file_name = regular_file_name
        self.bold_file_name = bold_file_name
        self.italic_file_name = italic_file_name
        self.bold_italic_file_name = bold_italic_file_name

        self.info = {'name': self.name,
                     'size': self.size,
                     'bold': False,
                     'italic': False}


class UIFontDictionary(IUIFontDictionaryInterface):
    """
    The font dictionary is used to store all the fonts that have been loaded into the UI system.
    """
    _html_font_sizes = {
        1: 8,
        1.5: 9,
        2: 10,
        2.5: 11,
        3: 12,
        3.5: 13,
        4: 14,
        4.5: 16,
        5: 18,
        5.5: 20,
        6: 24,
        6.5: 32,
        7: 48
    }

    _html_font_sizes_reverse_lookup = {
        8: 1,
        9: 1.5,
        10: 2,
        11: 2.5,
        12: 3,
        13: 3.5,
        14: 4,
        16: 4.5,
        18: 5,
        20: 5.5,
        24: 6,
        32: 6.5,
        48: 7
    }

    def __init__(self, resource_loader: IResourceLoader, locale: str):
        # , use_threaded_loading: bool = False, loading_queue: ClosableQueue = None
        # self.use_threaded_loading = use_threaded_loading
        # self.loading_queue = loading_queue
        self._resource_loader = resource_loader

        # match up two letter locale ids with a font that supports their alphabet
        self._latin_font = DefaultFontData(14,
                                           'noto_sans',
                                           'regular',
                                           'NotoSans-Regular.ttf',
                                           'NotoSans-Bold.ttf',
                                           'NotoSans-Italic.ttf',
                                           'NotoSans-BoldItalic.ttf')

        self._symbols_font = DefaultFontData(14,
                                             'fira_code_symbols',
                                             'regular',
                                             'FiraCode-Regular.ttf',
                                             'FiraCode-Regular.ttf',
                                             'FiraCode-Regular.ttf',
                                             'FiraCode-Regular.ttf')

        self._japanese_font = DefaultFontData(14,
                                              'noto_sans_jp',
                                              'regular',
                                              'NotoSansJP-Regular.otf',
                                              'NotoSansJP-Bold.otf',
                                              'NotoSansJP-Regular.otf',
                                              'NotoSansJP-Bold.otf')
        self._chinese_font = DefaultFontData(14,
                                             'noto_sans_sc',
                                             'regular',
                                             'NotoSansSC-Regular.otf',
                                             'NotoSansSC-Bold.otf',
                                             'NotoSansSC-Regular.otf',
                                             'NotoSansSC-Bold.otf')
        self._korean_font = DefaultFontData(14,
                                            'noto_sans_kr',
                                            'regular',
                                            'NotoSansKR-Regular.ttf',
                                            'NotoSansKR-Bold.ttf',
                                            'NotoSansKR-Regular.ttf',
                                            'NotoSansKR-Bold.ttf')
        self._hebrew_font = DefaultFontData(14,
                                            'noto_sans_he',
                                            'regular',
                                            'NotoSansHebrew-Regular.ttf',
                                            'NotoSansHebrew-Bold.ttf',
                                            'NotoSansHebrew-Regular.ttf',
                                            'NotoSansHebrew-Bold.ttf',
                                            script='Hebr',
                                            direction=pygame.DIRECTION_RTL)
        self._arabic_font = DefaultFontData(14,
                                            'noto_sans_ar',
                                            'regular',
                                            'NotoSansArabic-Regular.ttf',
                                            'NotoSansArabic-Bold.ttf',
                                            'NotoSansArabic-Regular.ttf',
                                            'NotoSansArabic-Bold.ttf',
                                            script='Arab',
                                            direction=pygame.DIRECTION_RTL
                                            )

        self._georgian_font = DefaultFontData(14,
                                              'noto_sans_ge',
                                              'regular',
                                              'NotoSansGeorgian-Regular.ttf',
                                              'NotoSansGeorgian-Bold.ttf',
                                              'NotoSansGeorgian-Regular.ttf',
                                              'NotoSansGeorgian-Bold.ttf',
                                              script='Geor',
                                              direction=pygame.DIRECTION_LTR
                                              )

        self.default_font_dictionary = {'ar': self._arabic_font,
                                        'de': self._latin_font,
                                        'en': self._latin_font,
                                        'es': self._latin_font,
                                        'fr': self._latin_font,
                                        'ge': self._georgian_font,
                                        'he': self._hebrew_font,
                                        'id': self._latin_font,
                                        'it': self._latin_font,
                                        'ja': self._japanese_font,
                                        'ko': self._korean_font,
                                        'pl': self._latin_font,
                                        'pt': self._latin_font,
                                        'ru': self._latin_font,
                                        'uk': self._latin_font,
                                        'vi': self._latin_font,
                                        'zh': self._chinese_font,

                                        }

        try:
            self.default_font: DefaultFontData = self.default_font_dictionary[locale]
        except KeyError:
            self.default_font: DefaultFontData = self._latin_font

        self._default_symbols_font: DefaultFontData = self._symbols_font

        self.debug_font_size = 8

        self.loaded_fonts = {}  # type: Dict[str, FontResource]
        self.known_font_paths: Dict[str, List[Tuple[Union[str, PackageResource, bytes], bool]]] = {}

        self._load_default_font(self.default_font)
        self._load_default_font(self._default_symbols_font)

        self.used_font_ids = [self.default_font.idx, self._default_symbols_font.idx]

    def set_locale(self, new_locale: str):
        try:
            new_font = self.default_font_dictionary[new_locale]
        except KeyError:
            new_font = self._latin_font

        if self.default_font != new_font:
            self.default_font = new_font
            self._load_default_font(self.default_font)

    def _load_default_font(self, font):
        """
        Load a default font.

        """
        # TEMP select to load from str path or file bytes
        which = "str" # "bytes"
        print(f"TEMP ui_font_dictionary preloading from {which}")
        # just testing with default regular font for now
        if which == "bytes":
            with open(fonts_path(self.default_font.regular_file_name), "rb") as f:
                b = f.read()
            location = (b, False)
        elif which == "str":
            location = (fonts_path(self.default_font.regular_file_name), False)
        default_font_res = FontResource(
            font_id=font.idx,
            size=font.size,
            style={'bold': False, 'italic': False, 'antialiased': True,
                   'script': font.script, 'direction': font.direction},
            location=location
#             location=(
#                 PackageResource(package='pygame_gui.data',
#                                 resource=font.regular_file_name),
#                 False)
        )

        # TEMP loading default font
        print("TEMP loading default font", self.default_font.idx)
        error = default_font_res.load()
        if error is not None and isinstance(error, Exception):
            raise error

        self.loaded_fonts[font.idx] = default_font_res

        # TEMP avoiding PackageResource, using string paths
        self.known_font_paths[font.name] = [
            (fonts_path(self.default_font.regular_file_name), False),
            (fonts_path(self.default_font.bold_file_name), False),
            (fonts_path(self.default_font.italic_file_name), False),
            (fonts_path(self.default_font.bold_italic_file_name), False)]
#             (PackageResource(package='pygame_gui.data',
#                              resource=font.regular_file_name), False),
#             (PackageResource(package='pygame_gui.data',
#                              resource=font.bold_file_name), False),
#             (PackageResource(package='pygame_gui.data',
#                              resource=font.italic_file_name), False),
#             (PackageResource(package='pygame_gui.data',
#                              resource=font.bold_italic_file_name), False)]

    def find_font(self, font_size: int, font_name: str,
                  bold: bool = False, italic: bool = False, antialiased: bool = True,
                  script: str = 'Latn', direction: int = pygame.DIRECTION_LTR) -> IGUIFontInterface:
        """
        Find a loaded font from the font dictionary. Will load a font if it does not already exist,
        and we have paths to the needed files, however it will issue a warning after doing so
        because dynamic file loading is normally a bad idea as you will get frame rate hitches
        while the running program waits for the font to load.

        Instead, it's best to preload all your needed files at another time in your program when
        you have more control over the user experience.

        :param font_size: The size of the font to find.
        :param font_name: The name of the font to find.
        :param bold: Whether the font is bold or not.
        :param italic: Whether the font is italic or not.
        :param antialiased: Whether the font is antialiased or not.
        :param script: The ISO 15924 script code used for text shaping as a string.
        :param direction: the direction of text e.g. left to right or right to left. An integer.

        :return IGUIFontInterface: Returns either the font we asked for, or the default font.

        """
        return self.find_font_resource(font_size, font_name, bold, italic, antialiased,
                                       script=script, direction=direction).loaded_font

    def find_font_resource(self, font_size: int, font_name: str,
                           bold: bool = False, italic: bool = False, antialiased: bool = True,
                           script: str = 'Latn', direction: int = pygame.DIRECTION_LTR) -> FontResource:
        """
        Find a loaded font resource from the font dictionary. Will load a font if it does not
        already exist, and we have paths to the needed files, however it will issue a warning
        after doing so because dynamic file loading is normally a bad idea as you will get frame
        rate hitches while the running program waits for the font to load.

        Instead, it's best to preload all your needed files at another time in your program when
        you have more control over the user experience.

        :param font_size: The size of the font to find.
        :param font_name: The name of the font to find.
        :param bold: Whether the font is bold or not.
        :param italic: Whether the font is italic or not.
        :param antialiased: Whether the font is antialiased or not.
        :param script: The ISO 15924 script code used for text shaping as a string.
        :param direction: the direction of text e.g. left to right or right to left. An integer.

        :return FontResource: Returns either the font resource we asked for, or the default font.

        """
        font_id = self.create_font_id(font_size, font_name, bold, italic, antialiased)

        if font_id not in self.used_font_ids:
            self.used_font_ids.append(font_id)  # record font usage for optimisation purposes

        if self.check_font_preloaded(font_id):  # font already loaded
            return self.loaded_fonts[font_id]
        elif font_name in self.known_font_paths:
            # we know paths to this font, just haven't loaded current size/style
            style_string = "regular"
            if bold and italic:
                style_string = "bold_italic"
            elif bold:
                style_string = "bold"
            elif italic:
                style_string = "italic"

            font_aliasing = "0"
            if antialiased:
                font_aliasing = "1"

            warning_string = ('Finding font with id: ' +
                              font_id +
                              " that is not already loaded.\n"
                              "Preload this font with {'name': "
                              "'" + font_name + "',"
                                                " 'point_size': " + str(font_size) + ","
                                                                                     " 'style': '" + style_string + "'," +
                              " 'antialiased': '" + font_aliasing +
                              "'}")
            warnings.warn(warning_string, UserWarning)
            self.preload_font(font_size, font_name, bold, italic, force_immediate_load=True, antialiased=antialiased,
                              script=script, direction=direction)
            return self.loaded_fonts[font_id]
        else:
            if self._load_system_font(font_id, font_size, font_name, bold,
                                      italic, antialiased, script, direction,
                                      force_immediate_load=True):
                return self.loaded_fonts[font_id]
            else:
                return self.loaded_fonts[self.default_font.idx]

    def _load_system_font(self, font_id: str,font_size: int, font_name: str,
                          bold: bool = False, italic: bool = False, antialiased: bool = True,
                          script: str = 'Latn', direction: int = pygame.DIRECTION_LTR,
                          force_immediate_load: bool = False) -> bool:
        # let's try and use the SystemFonts
        found_system_no_style_font_path = match_font(font_name, bold=False, italic=False)
        if bold or italic:
            found_system_font_path = match_font(font_name, bold, italic)
        else:
            found_system_font_path = found_system_no_style_font_path
        if found_system_no_style_font_path is not None and found_system_font_path is not None:
            if bold and italic and found_system_font_path is not None:
                self.add_font_path(font_name, font_path=found_system_no_style_font_path,
                                   bold_italic_path=found_system_font_path)
            elif bold and not italic and found_system_font_path is not None:
                self.add_font_path(font_name, font_path=found_system_no_style_font_path,
                                   bold_path=found_system_font_path)
            elif not bold and italic and found_system_font_path is not None:
                self.add_font_path(font_name, font_path=found_system_no_style_font_path,
                                   italic_path=found_system_font_path)
            else:
                self.add_font_path(font_name, font_path=found_system_no_style_font_path)

            self._load_single_font_style((found_system_no_style_font_path, False),
                                         font_id, font_size,
                                         font_style={'bold': True,
                                                     'italic': True,
                                                     'antialiased': antialiased,
                                                     'script': script,
                                                     'direction': direction},
                                         force_immediate_load=force_immediate_load
                                         )
            return True
        return False

    def get_default_font(self) -> IGUIFontInterface:
        """
        Grab the default font.

        :return: The default font.

        """
        return self.find_font(self.default_font.size, self.default_font.name)

    def get_default_symbol_font(self) -> IGUIFontInterface:
        return self.find_font(self._symbols_font.size, self._symbols_font.name)

    def create_font_id(self, font_size: int, font_name: str, bold: bool, italic: bool, antialiased: bool = True) -> str:
        """
        Create an id for a particularly styled and sized font from those characteristics.

        :param font_size: The size of the font.
        :param font_name: The name of the font.
        :param bold: Whether the font is bold styled or not.
        :param italic: Whether the font is italic styled or not.
        :param antialiased: Whether the font is antialiased or not.

        :return str: The finished font id.

        """
        if font_size <= 0:
            font_size = self.default_font.size
            warnings.warn("Font size less than or equal to 0", UserWarning)
        if bold and italic:
            font_style_string = "bold_italic"
        elif bold:
            font_style_string = "bold"
        elif italic:
            font_style_string = "italic"
        else:
            font_style_string = "regular"

        font_aliasing = "non_aa"
        if antialiased:
            font_aliasing = "aa"

        return font_name + "_" + font_style_string + "_" + font_aliasing + "_" + str(font_size)

    def preload_font(self, font_size: int, font_name: str,
                     bold: bool = False, italic: bool = False,
                     force_immediate_load: bool = False, antialiased: bool = True,
                     script: str = 'Latn', direction: int = pygame.DIRECTION_LTR):
        """
        Lets us load a font at a particular size and style before we use it. While you can get
        away with relying on dynamic font loading during development, it is better to eventually
        preload all your font data at a controlled time, which is where this method comes in.

        :param font_size: The size of the font to load.
        :param font_name: The name of the font to load.
        :param bold: Whether the font is bold styled or not.
        :param italic: Whether the font is italic styled or not.
        :param force_immediate_load: resource loading setup to immediately
                                     load the font on the main thread.
        :param antialiased: Whether the font is antialiased or not.
        :param script: The ISO 15924 script code used for text shaping as a string.
        :param direction: the direction of text e.g. left to right or right to left. An integer.

        """
        font_id = self.create_font_id(font_size, font_name, bold, italic, antialiased)
        if font_id in self.loaded_fonts:  # font already loaded
            warnings.warn('Trying to pre-load font id: ' +
                          font_id +
                          ' that is already loaded', UserWarning)
        elif font_name in self.known_font_paths:
            # we know paths to this font, just haven't loaded current size/style
            regular_path = self.known_font_paths[font_name][0]
            bold_path = self.known_font_paths[font_name][1]
            italic_path = self.known_font_paths[font_name][2]
            bold_italic_path = self.known_font_paths[font_name][3]
            if bold and italic:
                self._load_single_font_style(bold_italic_path,
                                             font_id,
                                             font_size,
                                             font_style={'bold': True,
                                                         'italic': True,
                                                         'antialiased': antialiased,
                                                         'script': script,
                                                         'direction': direction},
                                             force_immediate_load=force_immediate_load)

            elif bold:
                self._load_single_font_style(bold_path,
                                             font_id,
                                             font_size,
                                             font_style={'bold': True,
                                                         'italic': False,
                                                         'antialiased': antialiased,
                                                         'script': script,
                                                         'direction': direction},
                                             force_immediate_load=force_immediate_load)
            elif italic:
                self._load_single_font_style(italic_path,
                                             font_id,
                                             font_size,
                                             font_style={'bold': False,
                                                         'italic': True,
                                                         'antialiased': antialiased,
                                                         'script': script,
                                                         'direction': direction},
                                             force_immediate_load=force_immediate_load)
            else:
                self._load_single_font_style(regular_path,
                                             font_id,
                                             font_size,
                                             font_style={'bold': False,
                                                         'italic': False,
                                                         'antialiased': antialiased,
                                                         'script': script,
                                                         'direction': direction},
                                             force_immediate_load=force_immediate_load)
        else:
            if not self._load_system_font(font_id, font_size, font_name, bold,
                                          italic, antialiased, script, direction, force_immediate_load):
                warnings.warn('Trying to pre-load font id:' + font_id + ' with no paths set & its not a system font')

    def _load_single_font_style(self,
                                font_loc: Tuple[Union[str, PackageResource, bytes], bool],
                                font_id: str,
                                font_size: int,
                                font_style: Dict[str, bool],
                                force_immediate_load: bool = False):
        """
        Load a single font file with a given style.

        :param font_loc: Path to the font file.
        :param font_id: id for the font in the loaded 'fonts' dictionary.
        :param font_size: pygame font size.
        :param font_style: style dictionary (italic, bold, antialiased, all, some or none)

        """
        resource = FontResource(font_id=font_id,
                                size=font_size,
                                style=font_style,
                                location=font_loc)
        if self._resource_loader.started() or force_immediate_load:
            # TEMP loading single font
            print("TEMP loading single font", font_id)
            error = resource.load()
            if error is not None:
                warnings.warn(str(error))

        else:
            self._resource_loader.add_resource(resource)

        self.loaded_fonts[font_id] = resource

    def add_font_path(self,
                      font_name: str,
                      font_path: Union[str, PackageResource],
                      bold_path: Optional[Union[str, PackageResource]] = None,
                      italic_path: Optional[Union[str, PackageResource]] = None,
                      bold_italic_path: Optional[Union[str, PackageResource]] = None):
        """
        Adds paths to different font files for a font name.

        :param font_name: The name to assign to these font files.
        :param font_path: The path to the font's file with no particular style.
        :param bold_path: The path to the font's file with a bold style.
        :param italic_path: The path to the font's file with an italic style.
        :param bold_italic_path: The path to the font's file with a bold and an italic style.

        """
        if font_name in self.known_font_paths:
            return

        if isinstance(font_path, PackageResource):
            regular_font_loc: Union[str, PackageResource, bytes] = font_path
        else:
            regular_font_loc = os.path.abspath(font_path)

        self.known_font_paths[font_name] = [
            (regular_font_loc, False),
            (bold_path, False) if bold_path is not None else (regular_font_loc, False),
            (italic_path, False) if italic_path is not None else (regular_font_loc, False),
            (bold_italic_path, False) if bold_italic_path is not None
            else (regular_font_loc, False)]

    def print_unused_loaded_fonts(self):
        """
        Can be called to check if the UI is loading any fonts that we haven't used by the point
        this function is called. If a font is truly unused then we can remove it from our loading
        and potentially speed up the overall loading of the program.

        This is not a foolproof check because this function could easily be called before we have
        explored all the code paths in a project that may use fonts.
        """
        unused_font_ids = [key for key in self.loaded_fonts if key not in self.used_font_ids]
        if unused_font_ids:
            print('Unused font ids:')
            for font_id in unused_font_ids:
                point_size = int(font_id.split('_')[-1])
                html_size = UIFontDictionary._html_font_sizes_reverse_lookup[point_size]
                print(font_id + '(HTML size: ' + str(html_size) + ')')

    def convert_html_to_point_size(self, html_size: float) -> int:
        """
        Takes in an HTML style font size and converts it into a point font size.

        :param html_size: Size in HTML style.

        :return int: A 'point' font size.

        """
        if html_size in UIFontDictionary._html_font_sizes:
            return UIFontDictionary._html_font_sizes[html_size]
        else:
            return self.default_font.size

    def check_font_preloaded(self, font_id: str) -> bool:
        """
        Check if a font is already preloaded or not.

        :param font_id: The ID of the font to check for

        :return: True or False.

        """
        return font_id in self.loaded_fonts

    def ensure_debug_font_loaded(self):
        """
        Ensure the font we use for debugging purposes is loaded. Generally called after we start
        a debugging mode.

        """
        if not self.check_font_preloaded(self.default_font.name + '_'
                                         + self.default_font.style +
                                         '_' + str(self.debug_font_size)):
            self.preload_font(self.debug_font_size, self.default_font.name,
                              force_immediate_load=True)
