from telegram.update import Update

import logging

def get_attributes(need_attributes: tuple):
    def decorator(func):
        def wrapper(*args, **kwargs):
            update: Update = args[1]

            attributes = {
                'update': update,
                'context': args[2],
                'chat_id': update.effective_chat.id,
                'user_id': update.effective_user.id,
                'username': update.effective_user.username,
            }

            if update.effective_message is not None:
                attributes.update(
                    {
                        'message': update.effective_message.text,
                    }
                )

                logging.info(f"@{attributes['username']}: {attributes['message']}")

            if update.callback_query is not None:
                attributes.update(
                    {
                        'callback_data': update.callback_query.data,
                    }
                )

            kwargs = {}
            for attribute in attributes:
                for need_attribute in need_attributes:
                    if attribute == need_attribute:
                        kwargs.update(
                            {
                                attribute: attributes[attribute],
                            }
                        )

            if tuple(kwargs.keys()) == need_attributes:
                kwargs.update(
                    {
                        'self': args[0],
                    }
                )

                return func(**kwargs)
            else:
                return Exception('Func attributes != need attributes!')
        return wrapper
    return decorator
