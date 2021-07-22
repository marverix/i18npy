import unittest
import i18npy
import os


class TestModule(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        global i18n
        super().__init__(*args, **kwargs)
        p = os.path.dirname(__file__)
        jp_translation_path = os.path.join(p, "translations/jp.json")
        i18n = i18npy.i18n_load(jp_translation_path)
        self.lang_en = i18npy.load(os.path.join(p, "translations/en.json"))
        self.lang_jp = i18npy.load(jp_translation_path)
        self.lang_pl = i18npy.load(os.path.join(p, "translations/pl.json"))

    def test_translations_simple(self):
        KEY = "Cancel"

        self.assertEqual(
            i18n(KEY), "キャンセル",
            "Should use global translator"
        )
        self.assertEqual(
            self.lang_en.translate(KEY), "Cancel",
            "Should use English instance of translator"
        )
        self.assertEqual(
            self.lang_jp.translate(KEY), "キャンセル",
            "Should use Japanes instance of translator"
        )
        self.assertEqual(
            self.lang_pl.translate(KEY), "Anuluj",
            "Should use Polish instance of translator"
        )

    def test_pluralism_simple(self):
        KEY = "%n comments"

        self.assertEqual(
            i18n(KEY, 0), "0 コメント",
            "Should return proper translation for num=0"
        )
        self.assertEqual(
            i18n(KEY, 1), "1 コメント",
            "Should return proper translation for num=1"
        )
        self.assertEqual(
            i18n(KEY, 2), "2 コメント",
            "Should return proper translation for num=2"
        )

        self.assertEqual(
            self.lang_en.translate(KEY, None), "Comments disabled",
            "Should show fallback translation when num=None"
        )
        self.assertEqual(
            self.lang_en.translate(KEY, 0), "0 comments",
            "Should return proper translation for num=0"
        )
        self.assertEqual(
            self.lang_en.translate(KEY, 1), "1 comment",
            "Should return proper translation for num=1"
        )
        self.assertEqual(
            self.lang_en.translate(KEY, 2), "2 comments",
            "Should return proper translation for num=2"
        )

    def test_pluralism_complex(self):
        KEY = "Due in %n days"

        self.assertEqual(
            self.lang_en.translate(KEY, None), "Expired",
            "Should show fallback translation when num=None"
        )
        self.assertEqual(
            self.lang_en.translate(KEY, -2), "Due 2 days ago",
            "Should return proper translation for num=-2"
        )
        self.assertEqual(
            self.lang_en.translate(KEY, -1), "Due Yesterday",
            "Should return proper translation for num=-1"
        )
        self.assertEqual(
            self.lang_en.translate(KEY, 0), "Due Today",
            "Should return proper translation for num=0"
        )
        self.assertEqual(
            self.lang_en.translate(KEY, 1), "Due Tomorrow",
            "Should return proper translation for num=1"
        )
        self.assertEqual(
            self.lang_en.translate(KEY, 2), "Due in 2 days",
            "Should return proper translation for num=2"
        )

    def test_replacements(self):
        KEY = "Welcome %{name}"

        self.assertEqual(
            self.lang_en.translate(KEY, {"name": "John"}), "Welcome John",
            "Replacement should work even if KEY is not in dictionary"
        )

    def test_short_keys(self):
        self.assertEqual(
            i18n("_short_key", "This is a long piece of text"), "This is a long piece of text",
            "Should use default text"
        )
        self.assertEqual(
            i18n("_monkeys"), "猿も木から落ちる",
            "Should work normally"
        )

    def test_contexts_combined(self):
        KEY = "%{name} uploaded %n photos to their %{album} album"

        self.assertEqual(
            i18n(KEY, 1, {
                "name": "John",
                "album": "Buck's Night"
            }, {
                "gender": "male"
            }),
            "Johnは彼のBuck's Nightアルバムに写真1枚をアップロードしました",
            "Should use context for male gender"
        )
        self.assertEqual(
            i18n(KEY, 3, {
                "name": "Jane",
                "album": "Hen's Night"
            }, {
                "gender": "female"
            }),
            "Janeは彼女のHen's Nightアルバムに写真3枚をアップロードしました",
            "Should use context for female gender"
        )

        self.assertEqual(
            self.lang_en.translate(KEY, 1, {
                "name": "John",
                "album": "Buck's Night"
            }, {
                "gender": "male"
            }),
            "John uploaded 1 photo to his Buck's Night album",
            "Should use context for male gender"
        )
        self.assertEqual(
            self.lang_en.translate(KEY, 3, {
                "name": "Jane",
                "album": "Hen's Night"
            }, {
                "gender": "female"
            }),
            "Jane uploaded 3 photos to her Hen's Night album",
            "Should use context for female gender"
        )

        self.assertEqual(
            self.lang_pl.translate(KEY, 1, {
                "name": "John",
                "album": "Buck's Night"
            }, {
                "gender": "male"
            }),
            "John przesłał 1 zdjęcie do jego albumu Buck's Night",
            "Should use context for male gender"
        )
        self.assertEqual(
            self.lang_pl.translate(KEY, 3, {
                "name": "Jane",
                "album": "Hen's Night"
            }, {
                "gender": "female"
            }),
            "Jane przesłała 3 zdjęcia do jej albumu Hen's Night",
            "Should use context for female gender"
        )
        self.assertEqual(
            self.lang_pl.translate(KEY, 5, {
                "name": "John",
                "album": "Buck's Night"
            }, {
                "gender": "male"
            }),
            "John przesłał 5 zdjęć do jego albumu Buck's Night",
            "Should use context for male gender"
        )


if __name__ == "__main__":
    unittest.main()
