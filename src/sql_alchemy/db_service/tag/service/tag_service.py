from src.sql_alchemy.db_service.account.service import account_service
from src.sql_alchemy.db_model.account import Account
from src.sql_alchemy.db_model.account_tag_association import AccountTagAssociation
from src.sql_alchemy.db_model.tag import Tag
from src.sql_alchemy.service import db_session_service


def split_tags(tags: str | None) -> list[str]:
    if tags is None:
        return []
    return tags.split(',')


def select_or_create_tag_by_name(name: str) -> Tag:
    tag = db_session_service.get_session().query(Tag).filter(Tag.name == name).first()
    if tag is None:
        tag = Tag(name=name)
    return tag


def select_or_create_account_tag_association(account: Account, tag: Tag) -> AccountTagAssociation:
    account_tag_association = None
    if account.account_seq is not None and tag.tag_seq is not None:
        account_tag_association = db_session_service.get_session().query(AccountTagAssociation)\
            .filter(AccountTagAssociation.account_seq == account.account_seq)\
            .filter(AccountTagAssociation.tag_seq == tag.tag_seq).first()
    if account_tag_association is None:
        account_tag_association = AccountTagAssociation(account=account, tag=tag)
    return account_tag_association


def select_or_create_tags_by_names(names: list[str]) -> list[Tag]:
    tags = []
    for name in names:
        tags.append(select_or_create_tag_by_name(name))
    return tags


def insert_account_tags(account: Account, tags: list[Tag]):
    for tag in tags:
        account_tag_association = select_or_create_account_tag_association(account=account, tag=tag)
        account.tag_associations.append(account_tag_association)
    account_service.update_account(account)


def insert_account_tag_by_names(account: Account, names: list[str]):
    tags = select_or_create_tags_by_names(names=names)
    insert_account_tags(account=account, tags=tags)


def remove_account_tags(account: Account, tags: list[Tag]):
    for tag in tags:
        account_tag_association = select_or_create_account_tag_association(account=account, tag=tag)
        session = db_session_service.get_session()
        session.delete(account_tag_association)
        session.commit()


def remove_account_tag_by_names(account: Account, names: list[str]):
    tags = select_or_create_tags_by_names(names=names)
    remove_account_tags(account, tags)
