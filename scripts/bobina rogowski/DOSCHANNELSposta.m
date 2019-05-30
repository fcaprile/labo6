clear all;
format long;
clc;

%Defino la sesión VISA-USB
Osc = visa('tek','USB::0x0699::0x03A1::C012822::INSTR');

%incrementa el tamaño del buffer
set(Osc, 'Timeout', 20);
set(Osc,'InputBufferSize',2000000);

%abre la sesión Visa de comunicación con el osciloscopio
fopen(Osc);

%pide el nivel de trigger - dejo esto para ver que la comunicación funcione bien
trilev=query(Osc,'TRIG:MAI:LEV?');
N=1;
puntitos=zeros(2600,N);
%tiempito=zeros(2600,N);
puntitos2=zeros(2600,N);
%tiempito2=zeros(2600,N);

Par = query(Osc,'WFMPRE:XZE?;XIN?;YZE?;YMU?;CH1:YOFF?');
Par = str2num(Par);
XZE = Par(1);                                %time of ?rst data point in waveform
XIN = Par(2);                                %horizontal sampling interval
YZE = Par(3);                                %waveform conversion factor
YMU = Par(4);                                %vertical scale factor
YOFF1 = Par(5);                               %vertical position


Par2 = query(Osc,'WFMPRE:YZE?;YMU?;CH2:YOFF?');
Par2 = str2num(Par2);
YZE = Par2(1);                                %waveform conversion factor
YMU = Par2(2);                                %vertical scale factor
YOFF2 = Par2(3);                               %vertical position

for i=1:N

    OPC1=query (Osc, '*OPC?');
    fprintf(Osc,'ACQuire:STATE RUN'); 

%query(Osc,'ACQuire:NUMACq?')
fprintf(Osc,'ACQuire:STOPAfter SEQuence');
query (Osc, '*OPC?');
OPC2=query (Osc, '*OPC?');
[H1]=OSC1(Osc);   %adquiero canal 1
[H2]=OSC2(Osc);   %adquiero canal 2   

%query(Osc,'ACQuire:NUMACq?')
 
puntitos(1:length(H1),i)=H1;
%tiempito(1:length(tiempo1),i)=tiempo1;
puntitos2(1:length(H2),i)=H2;
%tiempito2(1:length(tiempo2),i)=tiempo2;
i
end

voltaje1=(puntitos-YOFF1)*YMU+YZE;
xend=XZE+XIN*length(puntitos)-XIN;
tiempo1=(XZE:XIN:xend)';

voltaje2=(puntitos2-YOFF2)*YMU+YZE;
xend=XZE+XIN*length(puntitos2)-XIN;
tiempo2=(XZE:XIN:xend)';
figure(1);
plot(tiempo1,voltaje1);
figure(2);
plot(tiempo2,voltaje2);


datoscanal1=[tiempo1 voltaje1];
filename_txt = ['datoscanal1_punta100_' datestr(now,'mmmm-dd-yyyy--HH-MM-SS') '.txt'];
save(filename_txt, 'datoscanal1','-ascii')

datoscanal2=[tiempo2 voltaje2];
filename_txt = ['datoscanal2_punta100' datestr(now,'mmmm-dd-yyyy--HH-MM-SS') '.txt'];
save(filename_txt, 'datoscanal2','-ascii')
%cambiar carpeta
%cierra la sesión
fclose(Osc)