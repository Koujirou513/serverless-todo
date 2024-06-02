import { atom } from 'recoil';

const getInitialState = () => {
    const savedState = localStorage.getItem('userLoginState');
    return savedState ? JSON.parse(savedState) : '';
};

export const userLoginState = atom({
    key: 'userLoginState',
    default: getInitialState(),
    effects_UNSTABLE: [
        ({ onSet }) => {
            onSet(newValue => {
                // localStorageに新しい値を保存
                localStorage.setItem('userLoginState', JSON.stringify(newValue));
            });
        },
    ],
});