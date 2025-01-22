import unittest

from jptranslations_provider import is_japanese

class TestLang(unittest.TestCase):

    def test_hiragana(self):
        self.assertTrue(is_japanese("こんにちは"))

    def test_empty_string(self):
        self.assertFalse(is_japanese(""))

    def test_numbers_and_symbols(self):
        self.assertFalse(is_japanese("1234!@#"))

    def test_stars(self):
        self.assertFalse(is_japanese("★※☆"))

    def test_reference_mark_symbol(self):
        self.assertFalse(is_japanese(" ※The next goldsmith"))

    def test_reference_mark_symbol_gigi(self):
        self.assertFalse(is_japanese("NE※GIGIGI★※... BlAcK pEaRl RiNg...GaAaH, tHiS iS bY fAr ThE wOrSt PiEcE gReEnHoRn HaS eVeR cRaFtEd. ItS vErY eXiStEnCe OfFeNdS mE. i FeEl ViOlAtEd, So ViOlAtEd!"))

    def test_reference_mark_symbol_workshop(self):
        self.assertFalse(is_japanese("BZZZT...★※☆ <Emphasis>Your new ※★ workshop is equipped with the latest in ★※☆, allowing you to ※☆★※☆ the envy of your friends and neighbors!</Emphasis>"))

    def test_missing_text_indicator(self):
        self.assertFalse(is_japanese("（★未使用／削除予定★）"))

    def test_inline_code(self):
        self.assertFalse(is_japanese("Present a black pearl ring <Sheet(Addon,9,0)/> melded with a piety materia III to Serendipity."))

    def test_omikuji(self):
        self.assertTrue(is_japanese("大変幸いの多い運気です　導きを胸に留めて過ごしましょう"))

    def test_jp_vm_06401(self):
        self.assertTrue(is_japanese("万を超えし 失敗作の果て―― 魂なき器に 生命宿りし殿堂なり！"))

    def test_jp_vm_06401_ellipsis(self):
        self.assertTrue(is_japanese("フッ……"))

    def test_exclaimed(self):
        self.assertFalse(is_japanese("！！"))

    def test_questioned(self):
        self.assertFalse(is_japanese("？"))

    def test_ellipsis(self):
        self.assertFalse(is_japanese("..."))

    def test__ellipsis(self):
        self.assertFalse(is_japanese("……"))

    def test_dash(self):
        self.assertFalse(is_japanese("――"))

    def test_jp_vm_06401_inlinecode(self):
        self.assertTrue(is_japanese("無駄じゃなかったよ。 君と<RubyCharaters>FF0AE38386E3839FE382B9FF0AE3828FE3819FE38197</RubyCharaters>が共に戦ったことは……何ひとつとして。"))

    def test_speaker_col(self):
        self.assertFalse(is_japanese("TEXT_VOICEMAN_06401_000020_PANDAEMONIUM	"))

    def test_number(self):
        self.assertFalse(is_japanese("12"))

    def test_english_inlinecode(self):
        self.assertFalse(is_japanese("Plainly, there <Emphasis>is</Emphasis> none. They have no wealth, no power, and no worth. To the Ul'dahn way of thinking, they may as well not exist."))

    def test_VoiceMan_02300_jp_0(self):
        self.assertTrue(is_japanese("オメガ……。"))

    def test_VoiceMan_02300_jp_1(self):
        self.assertTrue(is_japanese("我々は、奴が「対バハムート兵器」とも呼ぶべきオメガを、 完全破壊するためだったのではないかと睨んでいる。"))

    def test_VoiceMan_02300_jp_2(self):
        self.assertTrue(is_japanese("「シルフの仮宿」に、双蛇党の者を派遣しています。 詳しい話は、その者からお聞きください。"))

    def test_VoiceMan_02300_jp_3(self):
        self.assertTrue(is_japanese("(-？？？？-)……フフッ。"))

    def test_VoiceMan_02300_jp_4(self):
        self.assertFalse(is_japanese("。"))

    def test_oVoiceMan_06300_0(self):
        self.assertTrue(is_japanese("っ！"))

    def test_oVoiceMan_06300_1(self):
        self.assertTrue(is_japanese("くっ…"))

    def test_oVoiceMan_06300_2(self):
        self.assertFalse(is_japanese("(-Y'shtola-)Cagnazzo and Azdaja's eye were a diversion."))

    def test_spaces(self):
        self.assertFalse(is_japanese("          "))

    def test_spaces(self):
        self.assertTrue(is_japanese("      っ    "))

    def test_english_japanese_mix(self):
        self.assertTrue(is_japanese("This is a test こんにちは"))

    def test_japanese_with_special_characters(self):
        self.assertTrue(is_japanese("こんにちは! 今日はどうですか？"))

    def test_japanese_with_numbers(self):
        self.assertTrue(is_japanese("今日は2023年です"))

    def test_spaces_only(self):
        self.assertFalse(is_japanese("        "))

    def test_text_with_line_breaks(self):
        self.assertTrue(is_japanese("Hello\nこんにちは\nGoodbye"))

    def test_unwanted_symbol_phrase(self):
        self.assertFalse(
            is_japanese("Some text before（★未使用／削除予定★）Some text after"))

    def test_katakana_only(self):
        self.assertTrue(is_japanese("カタカナだけ"))

    def test_kanji_only(self):
        self.assertTrue(is_japanese("漢字だけ"))

    def test_hiragana_only(self):
        self.assertTrue(is_japanese("ひらがなだけ"))

    def test_only_punctuation(self):
        self.assertFalse(is_japanese("！？。"))

    def test_japanese_word_in_english_sentence(self):
        self.assertTrue(
            is_japanese("I like sushi, 寿司 is delicious."))

    def test_ruby_annotation_in_text(self):
        self.assertTrue(is_japanese(
            "無駄じゃなかったよ。 君と<RubyCharaters>FF0AE38386E3839FE382B9FF0AE3828FE3819FE38197</RubyCharaters>が共に戦ったことは……何ひとつとして。"))

    def test_halfwidth_characters(self):
        self.assertFalse(
            is_japanese("ﾋﾗｶﾞﾅ"))

    def test_emoji_characters(self):
        self.assertFalse(is_japanese("😀😁😂😎"))

    def test_fullwidth_punctuation(self):
        self.assertFalse(is_japanese("「」"))

    def test_numbers_only(self):
        self.assertFalse(is_japanese("1234567890"))

    def test_english_with_japanese_word(self):
        self.assertTrue(is_japanese("I have a pet 犬 named Fido."))

    def test_french_with_accents(self):
        self.assertFalse(is_japanese("C'est un joli garçon!"))

    def test_spanish_with_accents(self):
        self.assertFalse(is_japanese("¡Hola! ¿Cómo estás?"))

    def test_german_with_umlauts(self):
        self.assertFalse(is_japanese("Über den Wolken"))

    def test_portuguese_with_tilde(self):
        self.assertFalse(is_japanese("Não sei o que fazer."))
    
    def test_italian_with_accented_letters(self):
        self.assertFalse(is_japanese("Caffè e pasta"))  

    def test_czech_with_diacritics(self):
        self.assertFalse(is_japanese("Děkuji za pomoc!"))  

    def test_swedish_with_special_characters(self):
        self.assertFalse(is_japanese("Hälsningar från Sverige!"))  

    def test_russian_with_cyrillic(self):
        self.assertFalse(is_japanese("Привет, как дела?"))  

    def test_arabic_with_arabic_script(self):
        self.assertFalse(is_japanese("مرحبًا، كيف حالك؟"))  

    def test_greek_text(self):
        self.assertFalse(is_japanese("Καλημέρα, πώς είστε;"))  

    def test_hebrew_text(self):
        self.assertFalse(is_japanese("שלום, מה שלומך?"))  

    def test_turkish_text(self):
        self.assertFalse(is_japanese("Merhaba, nasılsınız?"))  

    def test_vietnamese_text(self):
        self.assertFalse(is_japanese("Chào bạn, bạn khỏe không?"))  

    def test_european_characters_with_numbers(self):
        self.assertFalse(is_japanese("My phone number is 123-456-7890"))

    def test_chinese_text(self):
        self.assertTrue(is_japanese("这是一个测试"))

    def test_japanese_with_kanji(self):
        self.assertTrue(is_japanese("これはテストです"))

    def test_japanese_chinese_mixed(self):
        self.assertTrue(is_japanese("これはテストです，中文也可以检测"))

    def test_chinese_no_japanese(self):
        self.assertTrue(is_japanese("我爱学习"))

    def test_pure_japanese_hiragana(self):
        self.assertTrue(is_japanese("こんにちは"))

    def test_pure_japanese_katakana(self):
        self.assertTrue(is_japanese("コンニチハ"))

    def test_english_text(self):
        self.assertFalse(is_japanese("This is an English sentence."))

    @staticmethod
    def run_all_tests():
        # Load all the test cases from the TestDatabase class
        test_loader = unittest.TestLoader()
        test_suite = test_loader.loadTestsFromTestCase(TestLang)

        # Create a test runner and run the tests
        test_runner = unittest.TextTestRunner()
        result = test_runner.run(test_suite)
        return result
