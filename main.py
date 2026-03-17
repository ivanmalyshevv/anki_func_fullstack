
import random
import sys
import time


STOP_WORD = 'СТОП'


def load_words(filename):
    """
    Загружает пары 'слово, перевод' из текстового файла и формирует словарь.
    Args:
        filename (str): Имя файла для загрузки данных.
    Returns:
        Dict[str, str]: Словарь, где ключ — исходное слово, значение — перевод.
    Если файл не найден — выводит сообщение об ошибке и завершает выполнение
    программы с кодом 1.
    """
    words = {}
    try:
        with open(filename, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Игнорировать строки с лишними запятыми
                if line.count(',') != 1:
                    continue
                parts = line.split(',', 1)
                word = parts[0].strip()
                translation = parts[1].strip()
                words[word] = translation
        return words
    except FileNotFoundError:
        print(f'Ошибка: файл {filename} не найден.')
        sys.exit(1)


def print_statistics(score, total_time):
    """
    Выводит итоговую статистику: счет, общее и среднее время.

    Args:
        score (int): Количество правильных ответов.
        total_time (float): Общее время игры.
    """
    if score > 0:
        avg_time = total_time / score
        print(f'Ваш итоговый счет: {score}')
        print(
            f'Время игры: {total_time:.2f} секунд '
            f'(среднее время: {avg_time:.2f} сек.)'
        )
    else:
        print('Ваш итоговый счет: 0')
        print('Время игры: 0.00 секунд (среднее время: —)')


def ask_and_check(word, correct):
    """
    Спрашивает у пользователя перевод слова,
    возвращает флаги выхода, правильности и время ответа.

    Args:
        word (str): Слово для перевода.
        correct (str): Правильный перевод.

    Returns:
        Tuple[bool, bool, float]:
        (нужен_выход, правильный_ли_ответ, время_ответа)
    """
    print(f'Ваше слово: {word}')
    start = time.time()
    answer = input('Ваш перевод: ').strip()
    end = time.time()
    if answer.lower() == STOP_WORD.lower():
        return True, False, 0.0
    is_correct = answer.strip().lower() == correct.strip().lower()
    answer_time = end - start
    return False, is_correct, answer_time


def start_game(words):
    """
    Запускает игровой режим: пользователь переводит случайные слова.

    Args:
        words (Dict[str, str]): Словарь слов.
    """
    if not words:
        print('Словарь пуст. Добавьте слова для начала игры.')
        return
    print('Чтобы закончить, введите СТОП')
    score = 0
    total_time = 0.0
    word_list = list(words.items())
    while True:
        word, correct = random.choice(word_list)
        need_exit, is_correct, answer_time = ask_and_check(word, correct)
        if need_exit:
            print('Спасибо за игру!')
            break
        total_time += answer_time
        if is_correct:
            score += 1
            print(
                f'Верно! Время на ответ: {answer_time:.2f} секунд'
            )
        else:
            print(
                f'Неправильно, правильный ответ: {correct} '
                f'(Время на ответ: {answer_time:.2f} секунд)'
            )
    print_statistics(score, total_time)


def train_until_mistake(words):
    """
    Запускает режим "до первой ошибки":
    пользователь переводит слова до ошибки или выхода.

    Args:
        words (Dict[str, str]): Словарь слов.
    """
    if not words:
        print('Словарь пуст. Добавьте слова для начала игры.')
        return
    print('Режим: игра до первой ошибки! Чтобы выйти вручную, введите СТОП')
    score = 0
    total_time = 0.0
    word_list = list(words.items())
    while True:
        word, correct = random.choice(word_list)
        need_exit, is_correct, answer_time = ask_and_check(word, correct)
        if need_exit:
            print('Выход из режима по запросу пользователя.')
            break
        total_time += answer_time
        if is_correct:
            score += 1
            print(
                f'Верно! Всего очков: {score} '
                f'(ответ за {answer_time:.2f} секунд)'
            )
        else:
            print(
                f'Ошибка! Неверно. Правильный ответ: {correct}'
            )
            break
    print_statistics(score, total_time)


def add_words(words):
    """
    Добавляет новые пары 'слово — перевод' в словарь по запросу пользователя.

    Args:
        words (Dict[str, str]): Словарь слов.
    """
    print('Чтобы закончить, введите СТОП')
    while True:
        word = input('Введите слово: ').strip()
        if word.lower() == STOP_WORD.lower():
            break
        translation = input('Введите перевод: ').strip()
        if translation.lower() == STOP_WORD.lower():
            break
        words[word] = translation


def show_all_words(words):
    """
    Выводит на экран все пары 'слово - перевод' из словаря одной строкой.

    Args:
        words (Dict[str, str]): Словарь слов.
    """
    output = '; '.join(
        f'{word} - {translation}' for word, translation in words.items()
    )
    print(output)


def save_words(words, filename):
    """
    Сохраняет все пары 'слово, перевод' из словаря в текстовый файл.

    Args:
        words (Dict[str, str]): Словарь слов.
        filename (str): Имя файла для сохранения.

    Формат файла: одна пара — одна строка, разделитель — запятая.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for word, translation in words.items():
            f.write(f'{word}, {translation}\n')
    print(f'Было сохранено {len(words)} слов в файл {filename}.')


def main():
    """
    Основной цикл работы программы-тренажёра для изучения слов.
    """
    words = load_words()
    print(f'Было загружено {len(words)} слов из файла words.txt')
    while True:
        menu = (
            'Меню:\n'
            '    1. Начать игру\n'
            '    2. Добавить слова\n'
            '    3. Тренировка до первой ошибки\n'
            '    4. Вывод всех слов\n'
            '    5. Выход\n'
        )
        print(menu)
        menu_choice = input('Пункт меню: ')
        if menu_choice == '1':
            start_game(words)
        elif menu_choice == '2':
            add_words(words)
        elif menu_choice == '3':
            train_until_mistake(words)
        elif menu_choice == '4':
            show_all_words(words)
        elif menu_choice == '5':
            save_words(words, FILENAME)
            sys.exit()
        else:
            print('Неизвестный пункт меню')

        if __name__ == '__main__':
            main()
