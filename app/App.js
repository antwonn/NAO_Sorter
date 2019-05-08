/**
 *
 */

import React from 'react';
import {Platform, StyleSheet} from 'react-native';
import {createAppContainer, createBottomTabNavigator} from "react-navigation";
import {LaunchScreen} from './src/LaunchScreen';

const instructions = Platform.select({
    ios: 'Press Cmd+R to reload,\n' + 'Cmd+D or shake for dev menu',
    android:
        'Double tap R on your keyboard to reload,\n' +
        'Shake or press menu button for dev menu',
});

// type Props = {};
console.ignoredYellowBox = ['Warning: componentWillReceiveProps'];

export default class MyApp extends React.Component {
    render() {
        return (<App/>);
    }
}

const AppTabNavigator = createBottomTabNavigator({
    Launch: LaunchScreen,
    //Main: MainScreen
}, {

    navigationOptions: ({navigation}) => ({
        //define the icon for each tab here...
        tabBarIcon: ({focused, tintColor}) => {
            const {routeName} = navigation.state;

            let icon;
            switch (routeName) {
                case 'Launch':
                    //add icons here
                    break;
                case 'Main':
                    break;
            }

            return <Ionicons
                name={icon}
                size={25}
                color={tintColor}/>;
        },
    }),
    tabBarOptions: {
        initialRouteName: 'Launch',
        activeTintColor: '#fff',
        inactiveTintColor: '#ddd',
        style: {
            backgroundColor: 'white',
        }
    }
});

const App = createAppContainer(AppTabNavigator);

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F5FCFF',
    },
    welcome: {
        fontSize: 20,
        textAlign: 'center',
        margin: 10,
    },
    instructions: {
        textAlign: 'center',
        color: '#333333',
        marginBottom: 5,
    },
});
