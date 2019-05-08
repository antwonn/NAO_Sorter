import React, {Component} from 'react';
import {TextInput, Text, View, ImageBackground, Image, TouchableOpacity} from "react-native";

export class LaunchScreen extends Component {
    onPress = () => {
    }

    render() {
        return (
            <ImageBackground style={{
                flex: 1,
                justifyContent: 'space-evenly',
                alignItems: 'center',
                height: '100%',
                resizeMode: 'center',
            }}
                             source={require('../assets/NAO robot wave.jpg')}
            >
                <View style={{flex: 1, marginTop: '10%', alignItems: "center", justifyContent: "center"}}>
                    <Image style={{
                        flex: 1,
                        resizeMode: 'center',
                    }}
                           //source={require('./assets/loginscreen/.png')}
                    >
                    </Image>
                </View>

                <View style={{flex: 1, alignItems: "center", justifyContent: "center"}}>

                    <View style={{
                        flex: 1,
                        flexDirection: "row",
                        alignItems: "center",
                        justifyContent: "center",
                        margin: 20,
                    }}>
                        <View style={{flex: 1, alignItems: "center", justifyContent: "center",}}>

                            <TouchableOpacity onPress={this.onPress} style={{flex: 1, backgroundColor: "#4169e1", width: 80,}}>
                                <Text style={{
                                    color: 'white',
                                    fontSize: 24,
                                    fontWeight: 'bold',
                                    textAlignVertical: 'center',
                                    textAlign: 'center',
                                    marginVertical: 4,
                                }}>f</Text>
                            </TouchableOpacity>
                        </View>
                        <View style={{flex: 1, alignItems: "center", justifyContent: "center",}}>

                            <TouchableOpacity onPress={this.onPress} style={{flex: 1, backgroundColor: "#ff6347", width: 80,}}>
                                <Text style={{
                                    color: 'white',
                                    fontSize: 24,
                                    fontWeight: 'bold',
                                    textAlignVertical: 'center',
                                    textAlign: 'center',
                                    marginVertical: 4,
                                }}>g+</Text>
                            </TouchableOpacity>
                        </View>
                        <View style={{flex: 1, alignItems: "center", justifyContent: "center",}}>

                            <TouchableOpacity onPress={this.onPress} style={{flex: 1, backgroundColor: "yellow", width: 80,}}>
                                <Text style={{
                                    color: 'white',
                                    fontSize: 24,
                                    fontWeight: 'bold',
                                    textAlignVertical: 'center',
                                    textAlign: 'center',
                                    marginVertical: 4,
                                }}>S</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                    <View style={{
                        flex: 1,
                        backgroundColor: '#fa8072',
                        alignItems: "center",
                        justifyContent: "center",
                        padding: 2,
                    }}>
                        <TextInput
                            value=''
                            placeholder='Username'
                            placeholderColor='#fa8072'
                            style={{
                                flex: 1,
                                backgroundColor: 'black',
                                fontSize: 24,
                                color: '#fa8072',
                                width: 250,
                            }}>
                        </TextInput>
                    </View>
                    <View style={{
                        flex: 1,
                        backgroundColor: '#fa8072',
                        alignItems: "center",
                        justifyContent: "center",
                        padding: 2,
                    }}>
                        <TextInput
                            placeholder='Password'
                            placeholderColor='#fa8072'
                            secureTextEntry={true}
                            style={{
                                flex: 1,
                                backgroundColor: 'black',
                                fontSize: 24,
                                color: '#fa8072',
                                width: 250,
                            }}>
                        </TextInput>
                    </View>
                </View>
                <View style={{flex: 1, alignItems: "center", justifyContent: "center"}}>
                    <Text style={{color: 'white'}}>Forgot Password?</Text>
                    <View style={{
                        flex: 1,
                        flexDirection: 'row',
                        alignItems: "center",
                        justifyContent: "center",
                        overflow: 'hidden',
                        width: 250,
                    }}>
                        <TouchableOpacity onPress={this.onPress}
                                          style={{flex: 1, alignItems: 'center', backgroundColor: '#fa8072'}}>
                            <Text style={{fontSize: 30}}>Login</Text>
                        </TouchableOpacity>
                    </View>
                    <View style={{flex: 1, alignItems: "flex-start", justifyContent: "center"}}>
                        <Text style={{color: 'white'}}>Create a new account</Text>
                    </View>
                </View>
            </ImageBackground>
        );
    }
}
